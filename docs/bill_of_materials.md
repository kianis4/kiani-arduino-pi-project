# Bill of Materials

**Project:** Gesture-Controlled Robotic Hand
**Currency:** CAD (Canadian Dollars)
**Tax:** 13% HST (Ontario) applied as separate line item
**Note:** Search Amazon.ca for each item name. Prices are estimates as of March 2025.

## Core Electronics

| # | Item | Qty | Why We Need It | Est. Cost (CAD) |
|---|------|-----|----------------|-----------------|
| 1 | **Raspberry Pi 5 (8GB)** | 1 | Runs computer vision (MediaPipe hand tracking). 8GB handles camera + ML workload. | $115.00 |
| 2 | **Raspberry Pi 5 Official 27W USB-C Power Supply** | 1 | Pi 5 requires 5V/5A (27W). Third-party PSUs cause throttling. | $16.00 |
| 3 | **Raspberry Pi 5 Active Cooler** | 1 | Pi 5 thermal-throttles under sustained ML load without active cooling. | $8.00 |
| 4 | **Samsung EVO Plus 64GB microSD (A2/U3)** | 1 | Boot drive for Pi OS + project files. A2-rated for fast random I/O. | $14.00 |
| 5 | **Arduino Mega 2560 (Elegoo/clone)** | 1 | Servo controller. Mega has 4 hardware serial ports + ample pins for future expansion. | $22.00 |
| 6 | **PCA9685 16-Channel Servo Driver Board** | 1 | Generates jitter-free PWM for up to 16 servos over I2C (only 2 Arduino pins). Expandable. | $12.00 |

## Servos

| # | Item | Qty | Why We Need It | Est. Cost (CAD) |
|---|------|-----|----------------|-----------------|
| 7 | **MG996R Metal Gear Servo (pack of 8)** | 1 pack | 10 kg·cm torque, metal gears. Need 7 minimum (5 fingers + thumb abduction + wrist). 8th is spare/future wrist rotation. | $45.00 |

### Servo Assignment Plan
| Servo | Channel | Function |
|-------|---------|----------|
| S0 | CH0 | Thumb curl |
| S1 | CH1 | Index finger curl |
| S2 | CH2 | Middle finger curl |
| S3 | CH3 | Ring finger curl |
| S4 | CH4 | Pinky curl |
| S5 | CH5 | Thumb abduction (spread) |
| S6 | CH6 | Wrist bend (up/down) |
| S7 | CH7 | Wrist rotation (future) |

## Power System

| # | Item | Qty | Why We Need It | Est. Cost (CAD) |
|---|------|-----|----------------|-----------------|
| 8 | **6V 10A DC Power Supply (wall adapter, barrel jack)** | 1 | Dedicated servo power. 8 MG996R servos × ~1.2A stall = 9.6A peak. 10A gives headroom. 6V maximizes MG996R torque. | $25.00 |
| 9 | **DC Barrel Jack to Screw Terminal Adapter (5.5x2.1mm)** | 2 | Converts barrel jack to bare wire for easy connection to fuse/distribution. Spare included. | $8.00 |
| 10 | **Inline Blade Fuse Holder (ATC/ATO)** | 2 | Protects wiring from short circuits. One for servo rail, one spare. | $8.00 |
| 11 | **ATC Blade Fuses (10A, pack of 10)** | 1 | Replaceable fuses for the holders. 10A matches PSU rating. | $6.00 |
| 12 | **Screw Terminal Distribution Block (2x 4-position)** | 1 pack | Distributes power from PSU to multiple servo groups. Clean, re-configurable. | $10.00 |

## Wiring & Connectors

| # | Item | Qty | Why We Need It | Est. Cost (CAD) |
|---|------|-----|----------------|-----------------|
| 13 | **Dupont Jumper Wire Kit (M-M, M-F, F-F assortment)** | 1 | Breadboard connections, I2C wiring, signal wires. | $12.00 |
| 14 | **Full-Size Breadboard (830 tie points)** | 1 | Prototyping connections before permanent soldering. | $10.00 |
| 15 | **22 AWG Silicone Stranded Wire (6 colors, 10m each)** | 1 set | Power distribution wiring. 22AWG handles 7A+ which is plenty for branch wires. | $14.00 |
| 16 | **USB-A to USB-B Cable (1m)** | 1 | Connects Arduino Mega to Raspberry Pi (data + Arduino power). | $8.00 |
| 17 | **Heat Shrink Tubing Assortment** | 1 | Insulates solder joints and wire connections. Prevents shorts. | $10.00 |
| 18 | **Servo Extension Cables (30cm, pack of 10)** | 1 | Extends servo leads to reach PCA9685. Stock servo cables are short (~15cm). | $10.00 |

## Mechanical / Cable-Drive Components

| # | Item | Qty | Why We Need It | Est. Cost (CAD) |
|---|------|-----|----------------|-----------------|
| 19 | **Braided Fishing Line (80lb / 36kg test)** | 1 spool | Acts as finger tendons. Braided line is strong, thin, low-stretch, and knot-friendly. | $15.00 |
| 20 | **Small Spring Assortment Kit** | 1 | Return springs in finger joints (pulls fingers open when tendon releases). | $10.00 |
| 21 | **M2/M3 Screw + Nut Assortment Kit** | 1 | Mounts servos to forearm frame, assembles finger joints, attaches hand parts. | $14.00 |
| 22 | **PTFE Bowden Tube (2mm ID, 4mm OD, 2m)** | 1 | Low-friction cable guide for fishing line from forearm servos to fingers. Same tube used in 3D printers. | $8.00 |

## Optional but Recommended

| # | Item | Qty | Why We Need It | Est. Cost (CAD) |
|---|------|-----|----------------|-----------------|
| 23 | **Multimeter (basic digital)** | 1 | Essential for verifying voltages, checking continuity, debugging wiring. | $25.00 |
| 24 | **Raspberry Pi 5 Case (with fan cutout)** | 1 | Protects the Pi. Ensure it's compatible with the active cooler. | $12.00 |
| 25 | **Soldering Iron Kit (adjustable temp)** | 1 | For permanent connections once prototyping is done. Not needed immediately. | $30.00 |

## Cost Summary

| Category | Subtotal (CAD) |
|----------|----------------|
| Core Electronics (#1–6) | $187.00 |
| Servos (#7) | $45.00 |
| Power System (#8–12) | $57.00 |
| Wiring & Connectors (#13–18) | $64.00 |
| Mechanical (#19–22) | $47.00 |
| **Subtotal (Required)** | **$400.00** |
| Optional (#23–25) | $67.00 |
| **Subtotal (All)** | **$467.00** |
| HST 13% (on required) | $52.00 |
| HST 13% (on optional) | $8.71 |
| **Grand Total (Required + Tax)** | **$452.00** |
| **Grand Total (All + Tax)** | **$527.71** |

## Amazon.ca Search Tips

Since product links change frequently, search for these exact terms on Amazon.ca:

1. "Raspberry Pi 5 8GB" — buy from official resellers (CanaKit, Pishop.ca)
2. "Raspberry Pi 5 27W power supply official"
3. "Raspberry Pi 5 active cooler"
4. "Samsung EVO Plus 64GB microSD"
5. "Elegoo Mega 2560 R3" — identical to Arduino Mega, 1/3 the price
6. "PCA9685 16 channel servo driver"
7. "MG996R servo 8 pack"
8. "6V 10A DC power supply adapter"
9. "DC barrel jack screw terminal adapter"
10. "Inline blade fuse holder ATC"
11. "ATC blade fuse 10A"
12. "Screw terminal block 4 position"
13. "Dupont jumper wire kit"
14. "Breadboard 830 points"
15. "22 AWG silicone wire kit"
16. "USB A to USB B cable"
17. "Heat shrink tubing assortment"
18. "Servo extension cable 30cm 10 pack"
19. "Power Pro braided fishing line 80lb"
20. "Small spring assortment kit"
21. "M2 M3 screw nut assortment kit"
22. "PTFE bowden tube 2mm ID 4mm OD"

## Budget Alternative (Under $250)

If you want to save money and upgrade later:

| Swap | Save | Trade-off |
|------|------|-----------|
| Raspberry Pi 5 4GB instead of 8GB | ~$25 | Tight on RAM if running other processes |
| SG90 servos instead of MG996R | ~$30 | Plastic gears strip under load, weak grip |
| Skip multimeter (borrow from lab) | ~$25 | McMaster eng labs have them |
| Skip soldering iron (use lab) | ~$30 | McMaster makerspace has them |
| 5V 6A PSU instead of 6V 10A | ~$10 | Less servo torque, less headroom |

**Budget path total: ~$280 + tax ≈ $316 CAD**

Not recommended if you want to grip objects — the MG996R servos and 6V 10A PSU are the "no-regrets" choices.
