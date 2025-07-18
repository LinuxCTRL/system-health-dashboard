#!/bin/bash

# System Health Dashboard Installation Script with Virtual Environment

set -e

echo "📊 System Health Dashboard Installation"
echo "======================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

# Create and activate virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Make scripts executable
chmod +x health_dashboard.py
chmod +x run.sh

# Create config directory
CONFIG_DIR="$HOME/.config/health-dashboard"
DATA_DIR="$HOME/.local/share/health-dashboard"
LOGS_DIR="$DATA_DIR/logs"
WEB_DIR="$DATA_DIR/web"

mkdir -p "$CONFIG_DIR"
mkdir -p "$DATA_DIR"
mkdir -p "$LOGS_DIR"
mkdir -p "$WEB_DIR"

# Create default config if it doesn't exist
CONFIG_FILE="$CONFIG_DIR/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚙️  Creating default configuration..."
    cat > "$CONFIG_FILE" << EOF
{
    "refresh_interval": 2,
    "theme": "dark",
    "layout": "full",
    "alerts": {
        "cpu_threshold": 80,
        "ram_threshold": 85,
        "disk_threshold": 90,
        "temp_threshold": 75,
        "load_threshold": 4.0,
        "desktop_notifications": true,
        "sound_alerts": false,
        "email_notifications": false
    },
    "web_dashboard": {
        "port": 8080,
        "host": "localhost",
        "ssl": false,
        "auth": false
    },
    "logging": {
        "enabled": false,
        "interval": 60,
        "retention_days": 30,
        "log_path": "$LOGS_DIR"
    },
    "display": {
        "show_processes": true,
        "process_count": 10,
        "show_network": true,
        "show_temperatures": true,
        "show_disk_io": true,
        "colored_output": true
    },
    "system": {
        "detect_cachyos": true,
        "optimize_for_arch": true,
        "monitor_gpu": true,
        "monitor_sensors": true
    }
}
EOF
fi

# Create alias for easy access
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALIAS_COMMAND="alias health-check='$SCRIPT_DIR/run.sh'"

# Add alias to shell configuration files
for shell_config in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.bash_profile"; do
    if [ -f "$shell_config" ]; then
        # Check if alias already exists
        if ! grep -q "alias health-check=" "$shell_config"; then
            echo "" >> "$shell_config"
            echo "# System Health Dashboard alias" >> "$shell_config"
            echo "$ALIAS_COMMAND" >> "$shell_config"
            echo "Alias added to $shell_config"
        else
            echo "Alias already exists in $shell_config"
        fi
    fi
done

# Detect system type and provide specific instructions
if [ -f "/etc/cachyos-release" ]; then
    SYSTEM_TYPE="CachyOS"
elif [ -f "/etc/arch-release" ]; then
    SYSTEM_TYPE="Arch Linux"
elif [ -f "/etc/debian_version" ]; then
    SYSTEM_TYPE="Debian/Ubuntu"
else
    SYSTEM_TYPE="Linux"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "🖥️  Detected System: $SYSTEM_TYPE"
echo ""
echo "USAGE OPTIONS:"
echo ""
echo "Option 1 - Use alias (recommended, restart terminal or run 'source ~/.bashrc'):"
echo "  health-check                    # Launch real-time dashboard"
echo "  health-check --detailed         # Show comprehensive system info"
echo "  health-check --alert            # Set up monitoring alerts"
echo "  health-check --web --port 8080  # Launch web dashboard"
echo ""
echo "Option 2 - Use runner script directly:"
echo "  ./run.sh --help"
echo "  ./run.sh --detailed"
echo ""
echo "Option 3 - Manual virtual environment:"
echo "  source venv/bin/activate"
echo "  python3 health_dashboard.py --help"
echo "  deactivate"
echo ""
echo "NEXT STEPS:"
echo "1. Restart your terminal or run: source ~/.bashrc"
echo "2. Test installation: health-check --help"
echo "3. Launch dashboard: health-check"
echo "4. Set up alerts: health-check --alert --cpu-threshold 80"
echo ""
echo "📁 Configuration: $CONFIG_DIR/config.json"
echo "📊 Logs: $LOGS_DIR"
echo "🌐 Web files: $WEB_DIR"
echo ""
if [ "$SYSTEM_TYPE" = "CachyOS" ]; then
    echo "🔥 CachyOS detected! This tool is optimized for your performance setup!"
fi
echo "📊 Monitor your system like a PRO with System Health Dashboard!"