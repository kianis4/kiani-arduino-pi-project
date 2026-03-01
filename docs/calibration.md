# Servo Calibration Guide

## Why Calibrate?

Every servo is slightly different. The "0 degrees" and "180 degrees" positions vary between individual MG996R units. Calibration maps each servo's actual physical range to consistent angle values so all fingers behave predictably.

## What You're Calibrating

For each servo, you need to find two values:
- **SERVO_MIN**: The PWM pulse width (in PCA9685 ticks) where the servo is at its minimum position
- **SERVO_MAX**: The PWM pulse width where the servo is at its maximum position

The PCA9685 uses 12-bit resolution (0–4095 ticks). Typical servo range:
- Min: ~102 ticks (~0.5ms pulse)
- Max: ~512 ticks (~2.5ms pulse)

But MG996R servos commonly work best in the range **150–600 ticks**.

## Calibration Procedure

### 1. Setup

- Wire one servo at a time to the PCA9685
- Ensure servo power supply is on
- Arduino is connected and firmware is uploaded
- Run the calibration script from the Pi:

```bash
python3 scripts/calibrate_servos.py
```

### 2. For Each Servo

The script will:
1. Ask which channel (0–7) you're calibrating
2. Start at the midpoint (375 ticks)
3. Let you adjust up/down with keyboard arrows
4. Ask you to find the "fully open" position → records as MIN
5. Ask you to find the "fully closed" position → records as MAX
6. Save the values to `config/servo_limits.json`

### 3. Physical Checks

While calibrating each finger:
- **Listen for grinding/buzzing** — the servo is hitting its mechanical stop. Back off a few ticks.
- **Check the fishing line tension** — at "closed" position, the line should be taut but the finger should curl naturally
- **Check the return spring** — at "open" position, the spring should fully extend the finger

### 4. Calibration File Format

The calibration script saves to `config/servo_limits.json`:

```json
{
  "servos": {
    "0": { "name": "thumb_curl",       "min": 150, "max": 550 },
    "1": { "name": "index_curl",       "min": 160, "max": 540 },
    "2": { "name": "middle_curl",      "min": 155, "max": 545 },
    "3": { "name": "ring_curl",        "min": 150, "max": 550 },
    "4": { "name": "pinky_curl",       "min": 160, "max": 530 },
    "5": { "name": "thumb_abduction",  "min": 200, "max": 450 },
    "6": { "name": "wrist_bend",       "min": 150, "max": 550 },
    "7": { "name": "wrist_rotation",   "min": 150, "max": 550 }
  }
}
```

## Angle-to-Pulse Mapping

Once calibrated, the Arduino firmware maps incoming angles (0–180°) to each servo's specific pulse range:

```
pulse = servo_min + (angle / 180.0) * (servo_max - servo_min)
```

This means "90 degrees" always means the same physical position for each servo, regardless of manufacturing variation.

## Re-Calibration

Re-calibrate if:
- You replace a servo
- A fishing line stretches or is re-tied
- You modify the 3D-printed finger mechanism
- Servos start drifting or seem inaccurate

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Servo buzzes at endpoint | Hitting mechanical stop | Reduce min/max by 10-20 ticks |
| Finger doesn't fully close | MAX value too low | Increase MAX during calibration |
| Finger doesn't fully open | Return spring too weak or MIN too high | Adjust spring tension or decrease MIN |
| Servo jitters at rest | Electrical noise or loose ground | Check common ground, add 100µF capacitor |
| Servo doesn't move at all | Wrong channel or no power | Verify V+ power and channel number |
