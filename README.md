# Gesture-Controlled Robotic Hand

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: In Development](https://img.shields.io/badge/Status-In%20Development-blue)]()
[![Hardware: Arduino + Pi](https://img.shields.io/badge/Hardware-Arduino%20%2B%20Pi%205-green)]()

> A 3D-printed cable-driven robotic hand that mirrors your real hand gestures in real-time using computer vision. Wave, grip, point — the robot hand follows.

**Built by:** [Suleyman Kiani](https://github.com/kianis4) (BASc Computer Science, MEng Computing & Software Engineering) and Sara Kiani (BEng Year 1) at McMaster University.

---

## Table of Contents

- [Demo](#demo)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Milestone Plan](#milestone-plan)
- [Serial Protocol](#serial-protocol)
- [Safety](#safety)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Demo

> Coming soon! We'll add a video/GIF of the hand in action here.

## How It Works

1. **Camera sees your hand** — A USB webcam captures video of your hand
2. **AI finds your fingers** — Google MediaPipe detects 21 key points on your hand (every joint + fingertip)
3. **Math extracts angles** — Python calculates how curled each finger is (0° = open, 180° = fist)
4. **Arduino receives commands** — Angles are sent over USB serial to an Arduino Mega
5. **Servos pull cables** — The Arduino drives 8 servos via a PCA9685 board, pulling fishing line "tendons"
6. **Robot hand mirrors you** — Each finger curls to match your real hand, in real-time

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│  VISION (Raspberry Pi 5)                                      │
│  USB Webcam ──▶ MediaPipe ──▶ Angle Calculation               │
└──────────────────────────┬────────────────────────────────────┘
                           │ USB Serial
                           │ Protocol: <S0:90,S1:45,...>
┌──────────────────────────▼────────────────────────────────────┐
│  CONTROL (Arduino Mega 2560)                                  │
│  Serial Parser ──▶ Smoothing ──▶ PCA9685 I2C ──▶ 8x Servos   │
└───────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────▼────────────────────────────────────┐
│  POWER (Dedicated 6V 10A PSU)                                 │
│  Wall Adapter ──▶ Fuse (10A) ──▶ Distribution ──▶ Servo Rail  │
│  Common ground shared with Arduino + PCA9685                  │
└───────────────────────────────────────────────────────────────┘
```

## Project Structure

```
kiani-arduino-pi-project/
├── vision/                     # Computer vision (Python, runs on Pi)
│   ├── hand_tracker.py         # Main program: webcam → angles → serial
│   └── requirements.txt        # Python dependencies
├── firmware/                   # Microcontroller code (C++, runs on Arduino)
│   ├── servo_controller/
│   │   └── servo_controller.ino  # Serial parser + servo driver
│   └── README.md               # Flashing instructions
├── mechanical/                 # Physical build files
│   ├── stl/                    # 3D printable STL files
│   ├── cad/                    # Source CAD files (AutoCAD/Fusion 360)
│   ├── assembly/               # Build photos and notes
│   └── README.md               # Print settings + assembly guide
├── docs/                       # All documentation
│   ├── bill_of_materials.md    # Full parts list with costs (~$452 CAD)
│   ├── wiring.md               # Complete wiring diagram + connections
│   ├── calibration.md          # Servo calibration walkthrough
│   ├── safety.md               # Electrical safety rules + checklists
│   └── build_paths.md          # Architecture options compared
├── scripts/                    # Utility scripts
│   ├── setup_pi.sh             # One-command Raspberry Pi setup
│   ├── calibrate_servos.py     # Interactive servo calibration tool
│   └── test_serial.py          # Test Arduino serial connection
├── config/                     # Generated config (not checked in)
├── .github/                    # GitHub templates
│   ├── ISSUE_TEMPLATE/         # Bug report, feature request, task templates
│   └── pull_request_template.md
├── CONTRIBUTING.md             # How to contribute
├── LICENSE                     # MIT License
└── README.md                   # You are here
```

## Quick Start

### What You Need
- All parts from [docs/bill_of_materials.md](docs/bill_of_materials.md) (~$452 CAD with tax)
- Access to a 3D printer (PLA or PETG)
- A computer to set things up (Mac, Windows, or Linux)

### Step 1: Set Up the Raspberry Pi

```bash
git clone https://github.com/kianis4/kiani-arduino-pi-project.git
cd kiani-arduino-pi-project
bash scripts/setup_pi.sh
```

### Step 2: Flash the Arduino

1. Install [Arduino IDE](https://www.arduino.cc/en/software)
2. Open `firmware/servo_controller/servo_controller.ino`
3. Install **Adafruit PWM Servo Driver Library** (Library Manager → search "Adafruit PWM")
4. Board: `Arduino Mega or Mega 2560` → Upload

### Step 3: Wire Everything

Follow [docs/wiring.md](docs/wiring.md) — connect PCA9685 to Arduino (I2C), servos to PCA9685, and the dedicated 6V power supply through the fuse.

### Step 4: Calibrate Servos

```bash
python3 scripts/calibrate_servos.py
```

### Step 5: Run It

```bash
python3 vision/hand_tracker.py
```

Hold your hand in front of the webcam. The robotic hand mirrors your gestures.

## Milestone Plan

Track our progress on the [GitHub Project Board](https://github.com/kianis4/kiani-arduino-pi-project/projects).

| Phase | What | Status |
|-------|------|--------|
| **1. Parts & Power** | Order parts, assemble power distribution, test servos | Not started |
| **2. Vision Pipeline** | Set up Pi, run hand tracking, test serial communication | Not started |
| **3. Mechanical Build** | 3D print hand, thread tendons, assemble | Not started |
| **4. Integration** | Connect everything end-to-end, tune and test gripping | Not started |
| **5. Polish & Expand** | Add wrist rotation, improve grip, build enclosure | Not started |

## Serial Protocol

The Raspberry Pi sends angle commands to the Arduino:

```
<S0:90,S1:45,S2:180,S3:30,S4:60,S5:90,S6:120,S7:90>
```

| Channel | Function | Range |
|---------|----------|-------|
| S0 | Thumb curl | 0–180° |
| S1 | Index finger curl | 0–180° |
| S2 | Middle finger curl | 0–180° |
| S3 | Ring finger curl | 0–180° |
| S4 | Pinky curl | 0–180° |
| S5 | Thumb abduction (spread) | 0–180° |
| S6 | Wrist bend (up/down) | 0–180° |
| S7 | Wrist rotation (future) | 0–180° |

## Safety

See [docs/safety.md](docs/safety.md) for the full guide. Critical rules:

1. **NEVER** power servos from the Arduino — use the dedicated 6V PSU
2. **ALWAYS** fuse the servo power line (10A inline fuse)
3. **ALWAYS** connect common ground between PSU, Arduino, and PCA9685
4. **ALWAYS** disconnect power before changing any wiring

## Documentation

| Document | What's In It |
|----------|-------------|
| [Bill of Materials](docs/bill_of_materials.md) | Every part, why you need it, estimated cost |
| [Wiring Guide](docs/wiring.md) | Step-by-step wiring with diagrams |
| [Calibration Guide](docs/calibration.md) | How to calibrate each servo |
| [Safety Guide](docs/safety.md) | Electrical safety rules and checklists |
| [Build Paths](docs/build_paths.md) | Architecture options we considered |
| [Mechanical Guide](mechanical/README.md) | 3D printing and assembly instructions |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We use:
- **GitHub Issues** for tracking all tasks and ideas
- **GitHub Projects** for our Kanban board
- **Pull Requests** for all code changes (even our own)

## License

[MIT](LICENSE) — Suleyman Kiani & Sara Kiani, 2025
