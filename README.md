# 🚪 AI-niform Turnstile Access Control System

> An integrated computer vision and hardware access control solution designed to automate school uniform compliance verification and turnstile gate management.

<div align="center">

[![GitHub Release](https://img.shields.io/github/v/release/ichiroyamazaki/AI-niform-Turnstile?style=flat-square&color=blue)](https://github.com/ichiroyamazaki/AI-niform-Turnstile/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=flat-square)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)](https://github.com/ichiroyamazaki/AI-niform-Turnstile/graphs/commit-activity)

</div>

---

## 🚀 Overview

**AI-niform-Turnstile** is the core capstone and operational repository for the automated school uniform detection and physical access control system built for STI College Balagtas. It links deep learning inference (YOLO-based uniform detection) directly with physical turnstile hardware and microcontroller interfaces to grant or deny entry based on dress code compliance.

---

## 💼 Corporate & Creator Credit

* **Developed by:** [Ichiro Yamazaki](https://github.com/ichiroyamazaki)
* **Organization:** GoForAll Worldwide Corporation

---

## ✨ Features

* **Real-Time Uniform Detection:** Utilizes Ultralytics YOLO models to scan individuals and determine proper school uniform adherence.
* **Automated Turnstile Actuation:** Interfaces with hardware controllers (Arduino/relays) to unlock physical turnstile barriers upon successful verification.
* **Access Logging & Alerts:** Records entry attempts, manages compliance states, and handles notifications or warnings for violations.
* **Modular Architecture:** Separates computer vision processing, UI dashboards, and hardware serial communication for smooth deployment.

---

## 🛠️ Tech Stack & Requirements

* **Language:** Python 3.8+ & C++ (Arduino)
* **Computer Vision & AI:** Ultralytics YOLO, OpenCV
* **Hardware & Interfacing:** Serial (UART) communication, Relay modules, Solenoid / Turnstile mechanisms

---

## 📦 Project Structure

```text
AI-niform-Turnstile/
├── ai/                 # YOLO model weights, datasets, and inference scripts
├── hardware/           # Arduino firmware and circuit/wiring diagrams
├── ui/                 # User interface / dashboard components
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable configuration template
└── README.md           # Project documentation
⚙️ Installation & Setup
1. Clone the Repository
Bash
git clone [https://github.com/ichiroyamazaki/AI-niform-Turnstile.git](https://github.com/ichiroyamazaki/AI-niform-Turnstile.git)
cd AI-niform-Turnstile
2. Install Python Dependencies
Bash
pip install -r requirements.txt
3. Configure Environment Variables
Copy .env.example to .env and configure your camera indices, serial ports, and model parameters:

Code snippet
CAMERA_INDEX=0
SERIAL_PORT=/dev/ttyUSB0
BAUD_RATE=9600
CONFIDENCE_THRESHOLD=0.75
4. Run the Application
Bash
python main.py
🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to fork the repository and open a pull request.

📜 License
Distributed under the MIT License. See LICENSE for more information.
