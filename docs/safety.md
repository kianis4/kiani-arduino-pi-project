# Safety Guide

## Electrical Safety

### Rule #1: Separate Servo Power
**NEVER power servos from the Arduino's 5V or VIN pin.**

MG996R servos draw up to 1.2A each at stall. Eight servos = 9.6A peak. The Arduino's voltage regulator can supply ~500mA total. Attempting to draw servo current from the Arduino will:
- Destroy the voltage regulator
- Cause brownouts and erratic behavior
- Potentially start a fire

**Always use the dedicated 6V 10A power supply through the PCA9685's V+ screw terminal.**

### Rule #2: Always Fuse the Servo Power Line
The inline fuse (10A ATC) sits between the PSU and the distribution block. If a wire shorts or a servo fails:
- **With fuse:** Fuse blows, circuit is broken, no damage
- **Without fuse:** Wire heats up, insulation melts, potential fire

### Rule #3: Common Ground
All three systems must share a ground connection:
- 6V servo PSU ground
- Arduino ground
- PCA9685 ground

Without common ground, the I2C signals between Arduino and PCA9685 have no reference voltage, causing:
- Servos ignoring commands
- Random servo movements
- I2C communication errors

### Rule #4: Power-On Sequence
1. Connect all wiring (with power OFF)
2. Double-check connections with a multimeter
3. Power on the Arduino first (via USB)
4. Power on the servo PSU second
5. Run a test command to verify

**Power-off in reverse order:** servo PSU first, then Arduino.

## Mechanical Safety

### Servo Pinch Hazard
MG996R servos have significant torque (10 kg·cm). A closing robotic hand can pinch fingers.
- Keep hands clear of the mechanism when testing
- Start with slow movements during calibration
- Have the servo PSU power switch within easy reach

### 3D Print Integrity
- Inspect prints for cracks or delamination before assembly
- PLA becomes brittle with UV exposure — keep indoors
- PETG is stronger for load-bearing parts (finger joints)

### Fishing Line
- Braided fishing line under tension can snap and whip
- Wear eye protection when tensioning lines during assembly
- Cut excess line cleanly — frayed ends are hard to thread

## Debugging Safety

### Before Touching Any Wiring
1. Turn off servo PSU
2. Disconnect Arduino USB cable
3. Wait 5 seconds (capacitors discharge)
4. Verify 0V at distribution block with multimeter

### If Something Smells Like Burning
1. **Immediately** unplug the servo PSU
2. Unplug the Arduino USB
3. Do NOT touch any components (they may be hot)
4. Wait 2 minutes, then inspect for:
   - Darkened/melted components
   - Melted wire insulation
   - Burnt smell source
5. Identify the cause before re-powering

## Checklist Before Every Session

- [ ] All grounds connected (PSU, Arduino, PCA9685)
- [ ] Fuse installed in holder
- [ ] No bare wire exposed (heat shrink on all joints)
- [ ] Servo power comes from PSU, not Arduino
- [ ] Multimeter confirms correct voltage at V+ (5.5–6.5V)
- [ ] No loose connections or dangling wires
