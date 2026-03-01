# Contributing

Thanks for your interest in the Gesture-Controlled Robotic Hand project!

## Getting Started

1. Fork this repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/kiani-arduino-pi-project.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Push and open a Pull Request

## Branch Naming

Use these prefixes:
- `feature/` — New functionality (e.g., `feature/wrist-rotation`)
- `fix/` — Bug fixes (e.g., `fix/servo-jitter`)
- `docs/` — Documentation updates (e.g., `docs/wiring-photos`)
- `hardware/` — Mechanical or electrical changes (e.g., `hardware/finger-v2`)

## Commit Messages

Write clear commit messages that explain **what** and **why**:
```
Add wrist rotation servo support

Added channel 7 mapping for wrist rotation servo.
Updated serial protocol to include S7 in angle commands.
```

## Code Style

- **Python**: Follow PEP 8. Use descriptive variable names.
- **Arduino/C++**: Use camelCase for variables, UPPER_CASE for constants.
- **Comments**: Explain *why*, not *what*. The code should explain what.

## Reporting Issues

Use the issue templates provided. Include:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Photos/videos if it's a hardware issue

## Hardware Changes

If you modify the wiring or mechanical design:
- Update `docs/wiring.md` with any wiring changes
- Add photos to `mechanical/assembly/`
- Note any new parts needed in `docs/bill_of_materials.md`
