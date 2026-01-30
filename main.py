import json
import pyttsx3
import requests
from gpiozero import Button
from signal import pause

# --- Helper: Load Configuration ---
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

# --- Voice Engine Setup ---
def setup_voice(config):
    engine = pyttsx3.init()
    engine.setProperty('rate', config['voice_settings']['speed_wpm'])
    return engine

def speak(engine, text):
    print(f"elderberry says: {text}")
    engine.say(text)
    engine.runAndWait()

# --- Core Logic ---
class ElderberryApp:
    def __init__(self):
        self.config = load_config()
        if not self.config:
            print("Failed to initialize: config.json missing.")
            return

        self.engine = setup_voice(self.config)
        self.channel_index = 0
        self.channels = self.config['channels']
        
        # Setup Buttons from JSON mapping
        pins = self.config['hardware_mapping']
        self.btn_up = Button(pins['btn_up_gpio'])
        self.btn_down = Button(pins['btn_down_gpio'])
        self.btn_status = Button(pins['btn_status_gpio'])
        self.btn_msg = Button(pins['btn_message_gpio'])
        
        # Assign Actions
        self.btn_up.when_pressed = self.next_channel
        self.btn_down.when_pressed = self.prev_channel
        self.btn_status.when_pressed = self.announce_status
        self.btn_msg.when_pressed = self.read_messages

    def next_channel(self):
        self.refresh_data()
        self.channel_index = (self.channel_index + 1) % len(self.channels)
        self.trigger_tv_action()

    def prev_channel(self):
        self.refresh_data()
        self.channel_index = (self.channel_index - 1) % len(self.channels)
        self.trigger_tv_action()

    def announce_status(self):
        self.refresh_data()
        current_label = self.channels[self.channel_index]['label']
        speak(self.engine, f"You are watching {current_label}")

    def read_messages(self):
        """Fetches and reads the most recent message from Telegram."""
        token = self.config['telegram_settings']['bot_token']
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        
        try:
            response = requests.get(url, timeout=5).json()
            if response.get("result"):
                # Get the very last message in the updates list
                last_update = response["result"][-1]
                if "message" in last_update:
                    sender = last_update["message"]["from"].get("first_name", "Someone")
                    text = last_update["message"].get("text", "an empty message")
                    speak(self.engine, f"New message from {sender}. They said: {text}")
                else:
                    speak(self.engine, "You have a notification, but it is not a text message.")
            else:
                speak(self.engine, "You have no new messages.")
        except Exception as e:
            print(f"Message error: {e}")
            speak(self.engine, "I am sorry, I am having trouble checking your messages right now.")

    def refresh_data(self):
        # Reload config so changes to channels or settings take effect immediately
        latest_config = load_config()
        if latest_config:
            self.config = latest_config
            self.channels = latest_config['channels']

    def trigger_tv_action(self):
        label = self.channels[self.channel_index]['label']
        command = self.channels[self.channel_index]['command']
        speak(self.engine, label)
        # Placeholder for IR/CEC/Network TV control
        print(f"Action: Sending command '{command}' to TV")

# --- Execution ---
if __name__ == "__main__":
    app = ElderberryApp()
    print("elderberry system is active and listening...")
    speak(app.engine, "System online")
    pause()