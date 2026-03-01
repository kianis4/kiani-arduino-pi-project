#!/usr/bin/env bash
# Setup script for Raspberry Pi 5
# Run this once after cloning the repo on your Pi.
#
# Usage: bash scripts/setup_pi.sh

set -e

echo "========================================"
echo "  Robotic Hand — Raspberry Pi 5 Setup"
echo "========================================"

# Update system packages
echo "[1/5] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies for OpenCV and MediaPipe
echo "[2/5] Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    libopencv-dev \
    libatlas-base-dev \
    libhdf5-dev \
    v4l-utils \
    git

# Create Python virtual environment
echo "[3/5] Creating Python virtual environment..."
VENV_DIR="$(cd "$(dirname "$0")/.." && pwd)/venv"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Install Python packages
echo "[4/5] Installing Python packages..."
pip install --upgrade pip
pip install -r "$(dirname "$0")/../vision/requirements.txt"

# Add user to dialout group (required for serial access to Arduino)
echo "[5/5] Configuring serial port access..."
if ! groups "$USER" | grep -q dialout; then
    sudo usermod -aG dialout "$USER"
    echo "  Added $USER to 'dialout' group for serial access."
    echo "  YOU MUST LOG OUT AND BACK IN for this to take effect."
else
    echo "  $USER already in 'dialout' group."
fi

# Create config directory for calibration data
mkdir -p "$(dirname "$0")/../config"

echo ""
echo "========================================"
echo "  Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Log out and back in (if dialout group was added)"
echo "  2. Connect Arduino Mega via USB"
echo "  3. Activate the virtual environment:"
echo "       source venv/bin/activate"
echo "  4. Run the hand tracker:"
echo "       python3 vision/hand_tracker.py"
echo ""
