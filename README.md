# WIFI-QR-code-Generator  #Perfect Wi-Fi QR Generator

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![qrcode](https://img.shields.io/badge/qrcode-7.4+-yellowgreen.svg)

A sleek desktop application that generates scannable QR codes for Wi-Fi network credentials. Perfect for sharing your Wi-Fi with guests without revealing your password!


## Features ✨<img width="895" height="724" alt="Screenshot 2025-08-13 194736" src="https://github.com/user-attachments/assets/928d1156-4ec1-4e12-b551-b61f2ce732ba" />

- **Instant QR Generation**: Real-time updates as you type
- **Multiple Security Protocols**: Supports WPA/WPA2, WPA3, WEP, and open networks
- **Hidden Network Support**: Generates QR codes for non-broadcasting networks
- **High-Resolution Export**: Save crisp 600 DPI QR codes
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Modern UI**: Clean, intuitive interface with visual feedback

## Installation 💻

### Prerequisites
- Python 3.7+
- pip package manager

**Installation & Running**
  1. Install Python

**_Windows_**

* Download and install Python from https://www.python.org/.

* During setup check "Add Python to PATH".

* After install open PowerShell (or Command Prompt) and verify:
```
python --version
pip --version
python -m pip install --upgrade pip
```

2. requirements.txt

Create a file named requirements.txt in your project root with the following content:
```
qrcode>=7.4
PyQt5>=5.15.4
Pillow>=9.5.0
pyinstaller>=5.11
```

3. Install project dependencies

Open a terminal in your project directory and follow these steps (recommended: use a virtual environment).
Create and activate a virtual environment

Windows (PowerShell)
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows (CMD)
```
python -m venv venv
.\venv\Scripts\activate
```

Install packages from requirements.txt
```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
(If your system uses python3 and pip3, replace python with python3.)

Run the app

From the same terminal (with the virtual environment activated), run:
```
python main.py
```

Or, if your system uses python3:
```
python3 main.py
```

If the script is a PyQt GUI, a window should open. If nothing happens, run it with:
```
python -u main.py
```
to see runtime output/errors in the terminal.


_**Usage Guide 🚀**_
1. Enter your Wi-Fi network name (SSID)

2. Type your Wi-Fi password

3. Select security protocol:

~ WPA/WPA2 (most common)

~ WPA3 (latest security)

~ WEP (older networks)

~ None (open networks)

4. Check "Hidden network" if applicable

5. QR code updates automatically in real-time

6. Click "Save QR Code" to export as PNG

Tip: Print the QR code and place it where guests can easily scan it!


_** Troubleshooting 🔧**_
Problem: QR code doesn't scan

~ Solution: Ensure correct security protocol is selected

~ Solution: Verify password accuracy (case-sensitive)
