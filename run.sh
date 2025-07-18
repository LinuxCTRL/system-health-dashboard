#!/bin/bash

# System Health Dashboard Runner Script
# This script automatically activates the virtual environment and runs the tool

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found. Please run install_venv.sh first."
    exit 1
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Run the health dashboard with all passed arguments
python3 "$SCRIPT_DIR/health_dashboard.py" "$@"

# Keep virtual environment activated for user
echo ""
echo "💡 Virtual environment is still active. Run 'deactivate' to exit."