# Wiring Guide

## Overview

Three separate systems are wired together with a **common ground**:

```
                    COMMON GROUND BUS
          ┌──────────┬──────────────┬──────────────┐
          │          │              │              │
    ┌─────┴─────┐ ┌──┴──────┐ ┌────┴────┐  ┌──────┴──────┐
    │  Arduino  │ │ PCA9685 │ │ Servo   │  │ 6V 10A PSU  │
    │  Mega     │ │  Board  │ │ Rail    │  │ (wall adapter│
    │  2560     │ │         │ │ GND     │  │  GND output) │
    └─────┬─────┘ └──┬──────┘ └────┬────┘  └─────────────┘
          │          │              │
      USB to Pi   I2C (2 wire)   PWM to servos
```

## Step-by-Step Wiring

### 1. PCA9685 ↔ Arduino Mega (I2C)

| PCA9685 Pin | Arduino Mega Pin | Wire Color (suggested) |
|-------------|------------------|----------------------|
| VCC | 5V | Red |
| GND | GND | Black |
| SDA | SDA (Pin 20) | Blue |
| SCL | SCL (Pin 21) | Yellow |

**Note:** The PCA9685's VCC pin powers the board's logic chip only (not the servos). This is safe to power from Arduino's 5V.

### 2. Servo Power (CRITICAL — Read Carefully)

**DO NOT power servos from the Arduino. They MUST have a dedicated supply.**

```
6V 10A PSU                         PCA9685 Board
    │                                   │
    ├── + (positive) ──▶ FUSE (10A) ──▶ V+ terminal (screw terminal)
    │                                   │
    └── - (negative) ──────────────────▶ GND terminal (screw terminal)
                         │
                         └──────────────▶ Arduino GND (COMMON GROUND)
```

The PCA9685 has a separate screw terminal block labeled **V+** and **GND** specifically for servo power. This is where the 6V PSU connects.

### 3. Fusing the Servo Power Line

```
PSU (+) ──▶ [Inline Fuse Holder + 10A Fuse] ──▶ Distribution Block (+) ──▶ PCA9685 V+
PSU (-) ──▶ Distribution Block (-) ──▶ PCA9685 GND + Arduino GND
```

The fuse sits between the PSU and everything else. If a short circuit occurs, the fuse blows instead of melting wires or damaging components.

### 4. Connecting Servos to PCA9685

Each servo has a 3-wire connector (Brown/Red/Orange or Black/Red/White):

| Wire Color | Function | PCA9685 Pin |
|------------|----------|-------------|
| Brown/Black | GND | GND row |
| Red | V+ (power) | V+ row |
| Orange/White | Signal (PWM) | PWM row |

Plug each servo into its assigned channel:

| Channel | Servo Function |
|---------|---------------|
| CH0 | Thumb curl |
| CH1 | Index finger curl |
| CH2 | Middle finger curl |
| CH3 | Ring finger curl |
| CH4 | Pinky curl |
| CH5 | Thumb abduction |
| CH6 | Wrist bend |
| CH7 | Wrist rotation (future) |

### 5. Arduino ↔ Raspberry Pi

Simple USB connection:
- USB-B end → Arduino Mega
- USB-A end → Raspberry Pi 5

This provides:
- Serial communication (angle commands from Pi to Arduino)
- Power for the Arduino (5V from Pi's USB port — this is safe, Arduino draws ~50mA)

### 6. Webcam ↔ Raspberry Pi

- USB webcam → any USB-A port on the Pi

## Wiring Diagram (ASCII)

```
┌──────────────────────────────────────────────────────────────────┐
│                        6V 10A POWER SUPPLY                       │
│                     [Wall Adapter, barrel jack]                   │
└────────┬────────────────────────────┬────────────────────────────┘
         │ (+) Red                    │ (-) Black
         ▼                            │
  ┌──────────────┐                    │
  │  FUSE HOLDER │                    │
  │   (10A ATC)  │                    │
  └──────┬───────┘                    │
         │                            │
         ▼                            ▼
  ┌──────────────────────────────────────────┐
  │         DISTRIBUTION BLOCK               │
  │  (+) ─┬──────────────────┐               │
  │       │                  │               │
  │  (-) ─┼──────────────────┼───┐           │
  └───────┼──────────────────┼───┼───────────┘
          │                  │   │
          ▼                  │   ▼
   ┌──────────────┐          │  To Arduino GND
   │  PCA9685     │          │  (COMMON GROUND)
   │  V+ terminal │          │
   │  GND terminal│◀─────────┘
   │              │
   │  SDA ────────────────▶ Arduino Pin 20 (SDA)
   │  SCL ────────────────▶ Arduino Pin 21 (SCL)
   │  VCC ────────────────▶ Arduino 5V
   │  GND ────────────────▶ Arduino GND
   │              │
   │  CH0: Thumb curl      │
   │  CH1: Index curl      │
   │  CH2: Middle curl     │
   │  CH3: Ring curl       │
   │  CH4: Pinky curl      │
   │  CH5: Thumb abduction │
   │  CH6: Wrist bend      │
   │  CH7: (future)        │
   └──────────────┘
          │
     [Servo connectors: GND/V+/PWM]
          │
    ┌─────┴─────┐
    │  8x MG996R │
    │  Servos    │
    └───────────┘
```

## Common Ground Checklist

**All three of these GND points MUST be connected together:**

- [ ] PSU GND (-) → Distribution block GND
- [ ] Distribution block GND → PCA9685 GND screw terminal
- [ ] PCA9685 GND pin (header) → Arduino GND pin

Without common ground, servo signals will be unreliable and servos may jitter or not respond.

## Testing Sequence

1. **Before powering on:** Double-check all connections with a multimeter in continuity mode
2. **Power on PSU only (no Arduino):** Verify 6V at the PCA9685 V+ terminal
3. **Connect Arduino via USB:** Upload firmware, verify I2C communication
4. **Test one servo:** Connect a single servo to CH0, send test command
5. **Add servos one at a time:** Check that PSU voltage doesn't sag below 5.5V under load
6. **Full test:** All servos connected, run calibration script
