#!/usr/bin/env python3
"""
Interactive Servo Calibration Tool

Connects to the Arduino and lets you adjust each servo's min/max pulse width
interactively. Saves calibration data to config/servo_limits.json.

Usage:
    python3 scripts/calibrate_servos.py
    python3 scripts/calibrate_servos.py --port /dev/ttyACM0
"""

import argparse
import json
import os
import sys
import time

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("Error: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)


SERVO_NAMES = [
    "thumb_curl",
    "index_curl",
    "middle_curl",
    "ring_curl",
    "pinky_curl",
    "thumb_abduction",
    "wrist_bend",
    "wrist_rotation",
]

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "servo_limits.json")


def find_arduino():
    """Auto-detect Arduino serial port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        desc = port.description.lower()
        if any(kw in desc for kw in ["arduino", "mega", "ch340", "cp210", "usb serial"]):
            return port.device
    return None


def send_command(ser, channel, angle):
    """Send a single servo command to the Arduino."""
    # Build command with just the one servo we're testing
    cmd = f"<S{channel}:{angle}>\n"
    ser.write(cmd.encode())
    time.sleep(0.05)


def calibrate_servo(ser, channel):
    """Interactively calibrate a single servo channel."""
    name = SERVO_NAMES[channel] if channel < len(SERVO_NAMES) else f"channel_{channel}"
    print(f"\n{'='*50}")
    print(f"  Calibrating: {name} (Channel {channel})")
    print(f"{'='*50}")
    print()
    print("  Commands:")
    print("    +/=    Increase angle by 5")
    print("    -      Decrease angle by 5")
    print("    +10    Type a number to jump to that angle")
    print("    min    Set current position as MIN (fully open)")
    print("    max    Set current position as MAX (fully closed)")
    print("    done   Finish calibrating this servo")
    print("    skip   Skip this servo")
    print()

    current_angle = 90
    send_command(ser, channel, current_angle)
    print(f"  Starting at angle: {current_angle}")

    servo_min = None
    servo_max = None

    while True:
        prompt = f"  [{name}] angle={current_angle}"
        if servo_min is not None:
            prompt += f" min={servo_min}"
        if servo_max is not None:
            prompt += f" max={servo_max}"
        prompt += " > "

        try:
            user_input = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Calibration interrupted.")
            return None

        if user_input in ("+", "="):
            current_angle = min(180, current_angle + 5)
        elif user_input == "-":
            current_angle = max(0, current_angle - 5)
        elif user_input == "min":
            servo_min = current_angle
            print(f"  ✓ MIN set to {servo_min}")
            continue
        elif user_input == "max":
            servo_max = current_angle
            print(f"  ✓ MAX set to {servo_max}")
            continue
        elif user_input == "done":
            if servo_min is not None and servo_max is not None:
                return {"name": name, "min_angle": servo_min, "max_angle": servo_max}
            else:
                print("  ⚠ Set both min and max before finishing.")
                continue
        elif user_input == "skip":
            print(f"  Skipped {name}")
            return None
        else:
            try:
                current_angle = max(0, min(180, int(user_input)))
            except ValueError:
                print("  Invalid input. Use +, -, a number (0-180), min, max, done, or skip.")
                continue

        send_command(ser, channel, current_angle)
        print(f"  → Moved to {current_angle}°")


def main():
    parser = argparse.ArgumentParser(description="Interactive servo calibration")
    parser.add_argument("--port", type=str, default=None, help="Serial port")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    args = parser.parse_args()

    # Connect to Arduino
    port = args.port or find_arduino()
    if not port:
        print("Error: No Arduino detected. Connect Arduino and retry, or use --port.")
        sys.exit(1)

    print(f"Connecting to Arduino on {port}...")
    try:
        ser = serial.Serial(port, args.baud, timeout=1)
        time.sleep(2)  # Wait for Arduino reset
    except serial.SerialException as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Wait for READY signal
    deadline = time.time() + 5
    while time.time() < deadline:
        if ser.in_waiting:
            line = ser.readline().decode(errors="ignore").strip()
            if "READY" in line:
                print("Arduino is ready!")
                break
    else:
        print("Warning: Did not receive READY signal. Proceeding anyway...")

    # Load existing calibration if present
    calibration = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            calibration = json.load(f).get("servos", {})
        print(f"Loaded existing calibration from {CONFIG_FILE}")

    # Calibrate each servo
    print("\n" + "=" * 50)
    print("  SERVO CALIBRATION")
    print("  Calibrate each servo's min (open) and max (closed) angles.")
    print("  The physical pulse widths are handled by the Arduino firmware.")
    print("=" * 50)

    for channel in range(len(SERVO_NAMES)):
        result = calibrate_servo(ser, channel)
        if result:
            calibration[str(channel)] = result

    # Save calibration
    os.makedirs(CONFIG_DIR, exist_ok=True)
    output = {"servos": calibration}
    with open(CONFIG_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nCalibration saved to {CONFIG_FILE}")

    # Center all servos before exiting
    for ch in range(len(SERVO_NAMES)):
        send_command(ser, ch, 90)

    ser.close()
    print("Done! All servos centered.")


if __name__ == "__main__":
    main()
