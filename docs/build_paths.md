# Build Path Comparison

## Path A: Raspberry Pi 5 + Arduino Mega (RECOMMENDED)

```
Webcam → Pi 5 (MediaPipe) → USB Serial → Arduino Mega → PCA9685 → Servos
```

**Pros:**
- Fully standalone — no laptop needed for demos
- Pi 5 has a quad-core Cortex-A76 @ 2.4GHz — runs MediaPipe at 30+ FPS easily
- USB serial to Arduino is simple and reliable
- Can run headless (SSH in from laptop for development)
- Future-proof: add sensors, display, speech, etc. to the Pi later

**Cons:**
- Extra cost (~$140 for Pi 5 + PSU + SD + cooler)
- Initial Pi OS setup takes ~30 minutes
- Slightly more complex first-time setup than laptop

**Best for:** Portable demos, clean self-contained builds, engineering project presentations

---

## Path B: Laptop + Arduino Mega

```
Webcam → Laptop (MediaPipe) → USB Serial → Arduino Mega → PCA9685 → Servos
```

**Pros:**
- No Pi purchase — uses hardware you already have
- Easier to debug (full IDE, browser, terminal on laptop)
- Laptop GPU/CPU is typically faster than Pi 5

**Cons:**
- Always tethered to a laptop
- Not portable for demos (need laptop + long USB cable)
- Laptop runs other processes — MediaPipe may compete for resources

**Best for:** Budget builds, early prototyping before committing to Pi

---

## Path C: Raspberry Pi 5 Direct PWM (No Arduino)

```
Webcam → Pi 5 (MediaPipe + servo control) → PCA9685 (I2C) → Servos
```

**Pros:**
- Eliminates the Arduino entirely — fewer components
- Pi 5 can drive PCA9685 directly over I2C using Python (adafruit-circuitpython-pca9685)
- Simpler wiring, no serial protocol needed

**Cons:**
- Python I2C servo control has more latency than Arduino's C++ loop
- If Python crashes, servos may hold position indefinitely (Arduino firmware has safety timeout potential)
- Mixing real-time servo control with vision processing on one device
- Harder to add sensors later (Pi's GPIO is limited vs. Arduino's analog pins)

**Best for:** Minimal builds where simplicity is priority over robustness

---

## Recommendation: Path A

Path A (Pi 5 + Arduino) gives the best balance of:
1. **Separation of concerns** — Pi handles vision (high-level), Arduino handles servos (real-time)
2. **Reliability** — Arduino's 50Hz servo loop runs independently of Pi's processing load
3. **Portability** — Standalone unit for demos and presentations
4. **Expandability** — Arduino has analog pins for future sensors; Pi has USB/network for future features
5. **Learning value** — You learn both embedded (Arduino) and Linux computing (Pi) — valuable for engineering students

The extra ~$140 for the Pi is worth it for a project you want to showcase and build on.
