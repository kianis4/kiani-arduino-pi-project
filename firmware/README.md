# Firmware — Arduino Servo Controller

## Setup

1. Install [Arduino IDE](https://www.arduino.cc/en/software) (2.x recommended)
2. Open `servo_controller/servo_controller.ino`
3. Install dependencies via Library Manager (`Sketch → Include Library → Manage Libraries`):
   - **Adafruit PWM Servo Driver Library** (search "Adafruit PWM")
4. Select board: `Tools → Board → Arduino Mega or Mega 2560`
5. Select port: `Tools → Port → /dev/ttyACM0` (or whatever your Arduino shows as)
6. Upload

## Testing

After uploading, open the Serial Monitor (115200 baud). You should see:
```
READY
```

Send a test command:
```
<S0:0,S1:0,S2:0,S3:0,S4:0,S5:0,S6:90,S7:90>
```
This should move all finger servos to position 0 (open) with wrist centered.

## Configuration

Edit the calibration arrays in `servo_controller.ino` after running the calibration script:
```cpp
uint16_t servoMin[NUM_SERVOS] = {150, 150, 150, 150, 150, 200, 150, 150};
uint16_t servoMax[NUM_SERVOS] = {550, 550, 550, 550, 550, 450, 550, 550};
```

## Smoothing

The `MAX_STEP` constant controls how fast servos move per update cycle.
- Lower values = smoother but slower response
- Higher values = faster but more jerky
- Default: 5 degrees per cycle at ~50Hz = smooth and responsive
