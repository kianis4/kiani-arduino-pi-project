#!/usr/bin/env python3
"""
Hand Tracker — Detects hand landmarks via webcam and sends finger angles
to the Arduino over serial.

Uses Google MediaPipe for real-time hand landmark detection (21 keypoints).
Calculates finger curl angles and wrist bend, then transmits them as a
compact serial protocol to the Arduino servo controller.

Usage:
    python3 hand_tracker.py                    # auto-detect serial port
    python3 hand_tracker.py --port /dev/ttyACM0  # specify port
    python3 hand_tracker.py --no-serial        # vision only (no Arduino)
"""

import argparse
import math
import sys
import time

import cv2
import mediapipe as mp
import numpy as np

# Optional serial — allows running vision-only mode without Arduino
try:
    import serial
    import serial.tools.list_ports
    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False


# ---------------------------------------------------------------------------
# MediaPipe hand landmark indices (see mediapipe hand landmark diagram)
# ---------------------------------------------------------------------------
# Each finger has 4 landmarks: MCP (knuckle), PIP, DIP, TIP
# Wrist is landmark 0
FINGER_LANDMARKS = {
    "thumb":  [1, 2, 3, 4],
    "index":  [5, 6, 7, 8],
    "middle": [9, 10, 11, 12],
    "ring":   [13, 14, 15, 16],
    "pinky":  [17, 18, 19, 20],
}

WRIST = 0
MIDDLE_MCP = 9  # Used as reference for wrist bend angle


def calculate_angle(a, b, c):
    """Calculate angle at point b given three 3D points a, b, c.

    Returns angle in degrees (0-180).
    """
    ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = math.degrees(math.acos(cosine))
    return angle


def get_finger_curl(landmarks, finger_name):
    """Calculate curl angle for a finger (0 = straight/open, 180 = fully curled).

    Uses the angle at the PIP joint (middle joint of the finger) which is the
    primary contributor to curl/grip.
    """
    indices = FINGER_LANDMARKS[finger_name]
    mcp = landmarks[indices[0]]
    pip = landmarks[indices[1]]
    dip = landmarks[indices[2]]

    # Angle at PIP joint (the main "curl" joint)
    angle = calculate_angle(mcp, pip, dip)

    # Map: straight finger (~170°) → 0, curled finger (~40°) → 180
    curl = np.clip((170 - angle) / (170 - 40) * 180, 0, 180)
    return int(curl)


def get_thumb_abduction(landmarks):
    """Calculate thumb spread angle (how far thumb is from palm).

    Measures the angle between the thumb MCP and the index MCP relative to the wrist.
    """
    wrist = landmarks[WRIST]
    thumb_mcp = landmarks[1]
    index_mcp = landmarks[5]

    angle = calculate_angle(thumb_mcp, wrist, index_mcp)

    # Map: thumb close to palm (~20°) → 0, thumb spread (~80°) → 180
    abduction = np.clip((angle - 20) / (80 - 20) * 180, 0, 180)
    return int(abduction)


def get_wrist_bend(landmarks):
    """Calculate wrist bend (up/down) angle.

    Uses the angle between the wrist-to-middle-MCP vector and the vertical.
    """
    wrist = landmarks[WRIST]
    middle_mcp = landmarks[MIDDLE_MCP]

    # Vector from wrist to middle finger knuckle
    dy = middle_mcp.y - wrist.y  # Positive = hand pointing down in camera frame
    dx = middle_mcp.x - wrist.x

    # Angle from vertical (camera frame)
    angle = math.degrees(math.atan2(dx, dy))

    # Map to servo range: wrist neutral (~90°), bent up (~30°), bent down (~150°)
    wrist_servo = np.clip(angle + 90, 0, 180)
    return int(wrist_servo)


def find_serial_port():
    """Auto-detect Arduino serial port."""
    if not HAS_SERIAL:
        return None

    ports = serial.tools.list_ports.comports()
    for port in ports:
        desc = port.description.lower()
        if any(kw in desc for kw in ["arduino", "mega", "ch340", "cp210", "usb serial"]):
            print(f"[Serial] Auto-detected Arduino on {port.device}")
            return port.device

    # Fallback: common port names
    import platform
    if platform.system() == "Linux":
        for candidate in ["/dev/ttyACM0", "/dev/ttyUSB0"]:
            try:
                s = serial.Serial(candidate, timeout=0.1)
                s.close()
                return candidate
            except (serial.SerialException, OSError):
                pass
    elif platform.system() == "Darwin":
        for candidate in ["/dev/tty.usbmodem1101", "/dev/tty.usbserial-1420"]:
            try:
                s = serial.Serial(candidate, timeout=0.1)
                s.close()
                return candidate
            except (serial.SerialException, OSError):
                pass

    return None


def format_command(angles):
    """Format servo angles into the serial protocol string.

    Protocol: <S0:val,S1:val,...,S7:val>
    """
    parts = [f"S{i}:{angles[i]}" for i in range(len(angles))]
    return f"<{','.join(parts)}>\n"


def main():
    parser = argparse.ArgumentParser(description="Hand gesture tracking for robotic hand")
    parser.add_argument("--port", type=str, default=None, help="Serial port (auto-detect if omitted)")
    parser.add_argument("--baud", type=int, default=115200, help="Serial baud rate (default: 115200)")
    parser.add_argument("--no-serial", action="store_true", help="Run vision only, no serial output")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--show", action="store_true", default=True, help="Show camera feed with overlay")
    args = parser.parse_args()

    # --- Serial Setup ---
    ser = None
    if not args.no_serial:
        if not HAS_SERIAL:
            print("[Warning] pyserial not installed. Running in vision-only mode.")
            print("         Install with: pip install pyserial")
        else:
            port = args.port or find_serial_port()
            if port:
                try:
                    ser = serial.Serial(port, args.baud, timeout=1)
                    time.sleep(2)  # Arduino resets on serial connect
                    print(f"[Serial] Connected to {port} at {args.baud} baud")
                except serial.SerialException as e:
                    print(f"[Serial] Failed to connect: {e}")
                    print("[Serial] Running in vision-only mode.")
            else:
                print("[Serial] No Arduino detected. Running in vision-only mode.")
                print("         Connect Arduino and restart, or use --port to specify.")

    # --- MediaPipe Setup ---
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    )

    # --- Camera Setup ---
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"[Error] Cannot open camera {args.camera}")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print("[Camera] Opened successfully. Press 'q' to quit.")

    # --- Main Loop ---
    prev_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[Error] Failed to read frame")
                break

            # Flip horizontally for mirror effect
            frame = cv2.flip(frame, 1)

            # Convert BGR → RGB for MediaPipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            angles = [90, 90, 90, 90, 90, 90, 90, 90]  # Default: all servos centered

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                lm = hand.landmark

                # Calculate angles for each finger
                angles[0] = get_finger_curl(lm, "thumb")
                angles[1] = get_finger_curl(lm, "index")
                angles[2] = get_finger_curl(lm, "middle")
                angles[3] = get_finger_curl(lm, "ring")
                angles[4] = get_finger_curl(lm, "pinky")
                angles[5] = get_thumb_abduction(lm)
                angles[6] = get_wrist_bend(lm)
                # angles[7] = wrist rotation (future)

                # Draw hand landmarks on frame
                if args.show:
                    mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                # Send to Arduino
                cmd = format_command(angles)
                if ser:
                    ser.write(cmd.encode())

            # FPS counter
            now = time.time()
            fps = 1.0 / (now - prev_time + 1e-8)
            prev_time = now

            if args.show:
                # Display angle values on frame
                labels = ["Thumb", "Index", "Middle", "Ring", "Pinky", "ThumbAbd", "Wrist", "WristRot"]
                for i, (label, val) in enumerate(zip(labels, angles)):
                    color = (0, 255, 0) if results.multi_hand_landmarks else (0, 0, 255)
                    cv2.putText(frame, f"{label}: {val}", (10, 30 + i * 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

                cv2.putText(frame, f"FPS: {fps:.1f}", (540, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                serial_status = "CONNECTED" if ser else "NO SERIAL"
                cv2.putText(frame, serial_status, (480, 460),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0) if ser else (0, 0, 255), 1)

                cv2.imshow("Hand Tracker — Press Q to Quit", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except KeyboardInterrupt:
        print("\n[Info] Interrupted by user")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if ser:
            ser.close()
        print("[Info] Cleaned up. Goodbye!")


if __name__ == "__main__":
    main()
