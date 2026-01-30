```markdown
# 🫐 elderberry: OS Setup & Hardening Guide

This guide details the process of transforming a standard Raspberry Pi into a hardened, production-ready appliance for vision-restricted users.

## 📋 Prerequisites
* **Hardware:** Raspberry Pi (4, 5, or Zero 2 W)
* **Storage:** 16GB+ MicroSD Card
* **Tool:** [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

---

## 🛠️ 1. Initial Image Flashing
Use the Raspberry Pi Imager to flash the OS with the following pre-configurations:

1. **Operating System:** `Raspberry Pi OS Lite (64-bit)`
2. **Advanced Settings (Gear Icon):**
    - [x] **Hostname:** `elderberry`
    - [x] **SSH:** Enable (Password Authentication)
    - [x] **User:** Set username (e.g., `pi`) and a password.
    - [x] **Wi-Fi:** Configure your local SSID and Password.
    - [x] **Locale:** Set your specific Time Zone and Keyboard layout.

---

## 💻 2. System Prep & Dependencies
Once the Pi boots, connect via your terminal:
```bash
ssh pi@elderberry.local

```

Run the following commands to install the core software stack:

```bash
# Update system repositories
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-venv alsa-utils espeak-ng

# Create project directory (strictly lowercase)
mkdir ~/elderberry
cd ~/elderberry
python3 -m venv venv
source venv/bin/activate

# Install Python libraries
pip install gpiozero pyttsx3 Flask

```

---

## 🔊 3. Audio Configuration (USB Speaker)

Since the **elderberry** project requires high-clarity voice feedback, a USB speaker is the primary output.

1. Plug in the USB speaker and identify the card number:
```bash
aplay -l

```


2. Set the USB speaker as the system default:
```bash
sudo nano /etc/asound.conf

```


3. Paste the following configuration (assuming the USB speaker is **Card 1**):
```text
pcm.!default {
    type hw
    card 1
}
ctl.!default {
    type hw
    card 1
}

```



---

## 🚀 4. Automatic Startup (systemd)

To ensure the app launches immediately on power-up:

1. Create the service file:
```bash
sudo nano /etc/systemd/system/elderberry.service

```


2. Paste the following configuration:
```ini
[Unit]
Description=elderberry accessibility remote
After=multi-user.target

[Service]
Type=idle
User=pi
WorkingDirectory=/home/pi/elderberry
ExecStart=/home/pi/elderberry/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

```


3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable elderberry.service

```



---

## 🔒 5. Hardening: Read-Only Mode

This prevents SD card corruption when the user unplugs the device without a proper shutdown.

1. Open the Pi configuration tool:
```bash
sudo raspi-config

```


2. Navigate to: `Performance Options` -> `Overlay File System`.
3. Select **Yes** (Enable Overlay FS).
4. Select **Yes** (Make boot partition read-only).
5. **Finish** and **Reboot**.

> [!IMPORTANT]
> To make changes to the code after this step, you must remount the disk as read-write:
> `sudo mount -o remount,rw /`
> After your changes, simply reboot to return to protected Read-Only mode.


