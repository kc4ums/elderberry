import json
import time
import pyttsx3
from gpiozero import Button
from signal import pause

# --- Configuration Loader ---
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()

# --- Voice Setup ---
engine = pyttsx3.init()
v_settings = config['voice_settings']
engine.setProperty('rate', v_settings['speed_wpm'])

def speak(text):
    print(f"Elderberry says: {text}")
    engine.say(text)
    engine.runAndWait()

# --- State Management ---
# We track which index in the "channels" list we are currently on
current_index = 0
channel_list = config['channels']

# --- Hardware Setup ---
# Pulling pin numbers directly from the JSON
pins = config['hardware_mapping']
btn_up = Button(pins['btn_up_gpio'])
btn_down = Button(pins['btn_down_gpio'])
btn_status = Button(pins['btn_status_gpio'])

# --- Actions ---
def change_channel(step):
    global current_index, channel_list
    # Refresh config in case caregiver changed something
    new_config = load_config()
    channel_list = new_config['channels']
    
    # Calculate new position (wraps around)
    current_index = (current_index + step) % len(channel_list)
    
    target_channel = channel_list[current_index]
    
    # 1. Provide Audio Feedback
    speak(target_channel['label'])
    
    # 2. Trigger TV Command (We'll build this next)
    print(f"Sending IR Code: {target_channel['ir_code']}")

def announce_status():
    current_channel = channel_list[current_index]['label']
    speak(f"You are watching {current_channel}")

# --- Linking Buttons to Functions ---
btn_up.when_pressed = lambda: change_channel(1)
btn_down.when_pressed = lambda: change_channel(-1)
btn_status.when_pressed = announce_status

# --- Start Up ---
print("Elderberry System Active.")
speak("System online.")
pause()