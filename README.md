# 🫐 elderberry

**An accessible, tactile television remote and communication hub for the vision-restricted, built on Raspberry Pi.**

`elderberry` is a physical interface designed to replace complex modern TV remotes with high-contrast, large-format arcade buttons and clear, slow-paced audio feedback. It bridges the gap between modern Smart TV technology and the specific accessibility needs of elderly users.

---

## ✨ Key Features

* **Tactile First:** Uses high-visibility, 100mm arcade buttons—no touchscreens or tiny plastic buttons.
* **Voice Feedback:** Every action (channel changes, volume, status, messages) is confirmed with clear Text-to-Speech (TTS).
* **Message Readout:** A dedicated button allows the user to listen to the latest incoming messages from caregivers via Telegram.
* **Caregiver Portal:** A flexible system where channel names and voice settings can be updated via a simple web interface.
* **Hardened for Reliability:** Uses an "unplug-safe" read-only filesystem to prevent SD card corruption.
* **Universal Compatibility:** Modular design to support Infrared (IR), HDMI-CEC, or Wi-Fi control.

---

## 🛠️ Hardware Requirements

* **Processor:** Raspberry Pi 4, 5, or Zero 2 W.
* **Input:** 4x Large Arcade Buttons (assigned to: Up, Down, Status, and Messages).
* **Audio:** USB-powered speaker (for high-volume, clear speech).
* **Enclosure:** A sturdy, high-contrast box with a weighted base.

---

## 📂 Repository Structure

| File | Purpose |
| :--- | :--- |
| `main.py` | The core Python script that listens for button presses and fetches messages. |
| `config.json` | Stores user-specific settings (channels, voice speed, pin mapping, API tokens). |
| `OS_SETUP.md` | **[Start Here]** Step-by-step guide to installing the OS and hardening the Pi. |
| `requirements.txt` | List of Python dependencies for the project. |

---

## 🚀 Quick Start

1.  **Prepare the OS:** Follow the detailed [OS_SETUP.md](./OS_SETUP.md) to flash your SD card and configure the system.
2.  **Clone the Project:**
    ```bash
    cd ~
    git clone [https://github.com/yourusername/elderberry.git](https://github.com/yourusername/elderberry.git)
    cd elderberry
    ```
3.  **Setup Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4.  **Launch:**
    ```bash
    python main.py
    ```

---

## 📝 Caregiver Configuration

The `config.json` file allows for instant updates to channels and messaging tokens.

```json
{
  "voice_settings": {
    "speed_wpm": 140,
    "language": "en-us"
  },
  "telegram_settings": {
    "bot_token": "YOUR_TOKEN_HERE"
  },
  "channels": [
    { "id": 1, "label": "BBC One", "command": "1" },
    { "id": 2, "label": "ITV", "command": "2" }
  ]
}