#!/usr/bin/env python3
"""
Serial Communication Test — Verify Pi ↔ Arduino connection.

Sends test commands and checks for responses. Use this to debug
serial issues before running the full hand tracker.

Usage:
    python3 scripts/test_serial.py
    python3 scripts/test_serial.py --port /dev/ttyACM0
"""

import argparse
import sys
import time

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("Error: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)


def find_arduino():
    """Auto-detect Arduino serial port."""
    ports = serial.tools.list_ports.comports()
    print("Available serial ports:")
    for port in ports:
        print(f"  {port.device} — {port.description}")
    for port in ports:
        desc = port.description.lower()
        if any(kw in desc for kw in ["arduino", "mega", "ch340", "cp210", "usb serial"]):
            return port.device
    return None


def main():
    parser = argparse.ArgumentParser(description="Test serial connection to Arduino")
    parser.add_argument("--port", type=str, default=None, help="Serial port")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    args = parser.parse_args()

    port = args.port or find_arduino()
    if not port:
        print("\nError: No Arduino detected.")
        print("  1. Is the Arduino connected via USB?")
        print("  2. Is the correct driver installed?")
        print("  3. Try: ls /dev/tty* (Linux/Mac) to see available ports")
        sys.exit(1)

    print(f"\nConnecting to {port} at {args.baud} baud...")
    try:
        ser = serial.Serial(port, args.baud, timeout=2)
        time.sleep(2)  # Arduino resets on connection
    except serial.SerialException as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Read startup message
    print("Waiting for Arduino startup message...")
    for _ in range(10):
        if ser.in_waiting:
            line = ser.readline().decode(errors="ignore").strip()
            print(f"  Arduino says: {line}")
            if "READY" in line:
                break

    # Test commands
    test_commands = [
        ("<S0:0,S1:0,S2:0,S3:0,S4:0,S5:90,S6:90,S7:90>", "All fingers open"),
        ("<S0:180,S1:180,S2:180,S3:180,S4:180,S5:90,S6:90,S7:90>", "All fingers closed (fist)"),
        ("<S0:90,S1:90,S2:90,S3:90,S4:90,S5:90,S6:90,S7:90>", "All servos centered"),
        ("<S1:180,S2:180,S3:180,S4:180>", "Index+middle+ring+pinky closed (point)"),
        ("<S0:90,S1:90,S2:90,S3:90,S4:90,S5:90,S6:90,S7:90>", "Reset to center"),
    ]

    print("\nRunning test sequence...")
    for cmd, description in test_commands:
        print(f"\n  Test: {description}")
        print(f"  Sending: {cmd}")
        ser.write(f"{cmd}\n".encode())
        time.sleep(1.5)  # Wait for servos to move

        input("  Press Enter to continue...")

    ser.close()
    print("\nSerial test complete! If servos moved correctly, your wiring is good.")


if __name__ == "__main__":
    main()
