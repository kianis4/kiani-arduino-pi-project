# Mechanical Design — Cable-Driven Robotic Hand

## Design Approach

This project uses a **cable-driven (tendon) design**:
- Servos are mounted in the **forearm** section
- Braided fishing line runs from each servo through **Bowden tubes** to the fingertips
- **Return springs** in each finger joint pull the finger open when the cable is released
- When the servo pulls the cable, the finger curls closed (grip)

This is the same approach used by:
- [InMoov](http://inmoov.fr/) — open-source humanoid robot
- [Dexhand](https://github.com/TheRobotStudio/V2.0-Dexhand) — modern cable-driven design
- Most prosthetic hand research projects

## Why Cable-Driven?

- Servos don't need to fit inside tiny finger joints
- Full-size servos (MG996R) give much more grip strength
- Easier to repair — swap a servo or re-thread a line
- Scales well — adding more DOF just means more cables

## Recommended Open-Source Designs

Browse these for inspiration or use directly:

1. **Dexhand V2** — Modern, well-documented, designed for MG996R servos
2. **InMoov Hand** — Battle-tested, huge community, good for beginners
3. **Robotic Hand by Ryan Gross** (Thingiverse) — Simpler, fewer parts

## 3D Printing Notes

### Material
- **PLA**: Good for prototyping. Sufficient for most parts except high-stress joints.
- **PETG**: Recommended for finger joints and load-bearing parts. More flexible and durable.

### Settings (PLA)
- Layer height: 0.2mm
- Infill: 30-50% (higher for structural parts)
- Walls: 3 perimeters minimum
- Supports: Yes, for overhangs > 45°
- Print orientation: Align with stress direction where possible

### Settings (PETG)
- Layer height: 0.2mm
- Infill: 40-60%
- Walls: 3-4 perimeters
- Bed temp: 70-80°C
- Nozzle temp: 230-245°C

## Assembly Order

1. Print all finger segments (proximal, middle, distal × 5 fingers)
2. Print palm plate and forearm mount
3. Assemble finger joints with M2 screws as pivot pins
4. Install return springs at each joint
5. Thread Bowden tubes from forearm to each finger channel
6. Mount servos in forearm bracket
7. Thread fishing line: servo horn → through Bowden tube → attach to fingertip
8. Tension each line and test individual finger curl
9. Mount wrist servo and linkage
10. Final assembly and cable management

## CAD Files

Place your AutoCAD / Fusion 360 / STL files in this directory:
```
mechanical/
├── stl/           # Printable STL files
├── cad/           # Source CAD files (AutoCAD, Fusion 360)
├── assembly/      # Assembly photos and notes
└── README.md      # This file
```
