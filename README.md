# 📊 System Health Dashboard

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com)
[![CachyOS](https://img.shields.io/badge/Optimized%20for-CachyOS-FF6B35?style=flat&logo=linux)](https://cachyos.org)

**Monitor your system like a PRO!** 🖥️⚡

_A beautiful, real-time system monitoring dashboard with alerts, historical tracking, and web interface. Perfect for developers who want to keep their systems running at peak performance._

## ✨ Features

- 📊 **Real-Time Dashboard** - Live CPU, RAM, disk, and network monitoring
- 🚨 **Smart Alerts** - Configurable thresholds with desktop notifications
- 📈 **Historical Tracking** - Performance trends and data logging
- 🌡️ **Temperature Monitoring** - CPU/GPU temps and thermal throttling detection
- 🔄 **Process Management** - Top processes with kill/nice capabilities
- 💾 **Disk Analytics** - Usage, I/O stats, and health monitoring
- 🌐 **Network Insights** - Bandwidth usage, connections, and traffic analysis
- 🎨 **Beautiful CLI** - Rich tables, live charts, and colorful output
- 🌐 **Web Dashboard** - Modern web interface for remote monitoring
- ⚡ **Performance Optimized** - Especially tuned for CachyOS and Arch Linux
- 🐍 **Virtual Environment** - Clean, isolated installation
- 🔧 **Highly Configurable** - Custom thresholds, refresh rates, and layouts

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/LinuxCTRL/system-health-dashboard.git
cd system-health-dashboard

# Install with virtual environment (recommended)
chmod +x install_venv.sh
./install_venv.sh

# Restart terminal or reload shell
source ~/.bashrc
```

### Basic Usage

```bash
# Launch real-time dashboard
health-check

# Show detailed system information
health-check --detailed

# Set up performance alerts
health-check --alert --cpu-threshold 80 --ram-threshold 90

# Start web dashboard
health-check --web --port 8080

# Log performance data
health-check --log --interval 30s
```

## 📋 Commands

### Core Commands

| Command        | Description                    | Example                                   |
| -------------- | ------------------------------ | ----------------------------------------- |
| `health-check` | Launch real-time dashboard     | `health-check`                            |
| `--detailed`   | Show comprehensive system info | `health-check --detailed`                 |
| `--alert`      | Set up monitoring alerts       | `health-check --alert --cpu-threshold 85` |
| `--web`        | Launch web dashboard           | `health-check --web --port 8080`          |

### Monitoring Commands

| Command       | Description             | Example                                   |
| ------------- | ----------------------- | ----------------------------------------- |
| `--log`       | Enable data logging     | `health-check --log --interval 60s`       |
| `--processes` | Show top processes      | `health-check --processes --top 20`       |
| `--network`   | Network monitoring mode | `health-check --network --interfaces all` |
| `--temps`     | Temperature monitoring  | `health-check --temps --celsius`          |

### Analysis Commands

| Command       | Description            | Example                              |
| ------------- | ---------------------- | ------------------------------------ |
| `--history`   | Show historical data   | `health-check --history --last-week` |
| `--report`    | Generate system report | `health-check --report --export pdf` |
| `--benchmark` | Run system benchmark   | `health-check --benchmark --quick`   |
| `--health`    | System health check    | `health-check --health --full-scan`  |

## 🛠️ Advanced Usage

### Real-Time Monitoring

```bash
# Basic dashboard with auto-refresh
health-check

# Detailed view with all metrics
health-check --detailed --refresh 2s

# Focus on specific components
health-check --cpu --ram --disk
health-check --network --temps
health-check --processes --top 15

# Custom layout and colors
health-check --layout compact --theme dark
health-check --layout full --theme matrix
```

### Alert Configuration

```bash
# Set up comprehensive alerts
health-check --alert \
  --cpu-threshold 80 \
  --ram-threshold 85 \
  --disk-threshold 90 \
  --temp-threshold 75 \
  --load-threshold 4.0

# Email notifications
health-check --alert --email admin@company.com --smtp-server smtp.gmail.com

# Desktop notifications
health-check --alert --desktop-notify --sound

# Custom alert scripts
health-check --alert --on-alert "/path/to/script.sh"
```

### Web Dashboard

```bash
# Launch web interface
health-check --web --port 8080 --host 0.0.0.0

# Secure web dashboard
health-check --web --port 8443 --ssl --auth

# Custom web configuration
health-check --web --config web-config.json --theme dark

# API mode for external tools
health-check --api --port 8081 --cors
```

### Data Logging & Analysis

```bash
# Start logging with custom interval
health-check --log --interval 30s --output /var/log/system-health/

# Export historical data
health-check --history --export csv --last-month
health-check --history --export json --date-range "2024-01-01,2024-01-31"

# Generate performance reports
health-check --report --pdf --include-charts
health-check --report --html --interactive-charts
```

## 📊 Sample Output

### Real-Time Dashboard

```
╭─────────────────────────────────────────────────────────────────────────────────╮
│                           🖥️  System Health Dashboard                           │
│                                CachyOS Linux                                   │
╰─────────────────────────────────────────────────────────────────────────────────╯

┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🔥 CPU Usage                                    🧠 Memory Usage                │
│ ████████████████████████████████████░░░░ 85.2%  ████████████████████░░░░░ 76.4% │
│ Cores: 8 | Freq: 3.8 GHz | Load: 2.1          Used: 12.2GB | Free: 3.8GB      │
│ Temp: 68°C | Throttling: No                    Swap: 2.1GB | Cached: 4.2GB     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ 💾 Disk Usage                                   🌐 Network Activity             │
│ / (SSD): ████████████████████████░░░░░░ 78.5%   ↓ 125.4 MB/s ↑ 45.2 MB/s      │
│ Used: 235GB | Free: 65GB | Total: 300GB        Packets: 15.2K/s | Errors: 0    │
│ I/O: 450 MB/s read | 120 MB/s write            Connections: 127 active         │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🔄 Top Processes                                                                │
│ PID    │ Name           │ CPU%  │ RAM%  │ Status    │ User     │ Command         │
│ 1234   │ firefox        │ 25.4  │ 18.2  │ Running   │ user     │ /usr/bin/firefox│
│ 5678   │ code           │ 15.8  │ 12.1  │ Running   │ user     │ /usr/bin/code   │
│ 9012   │ python         │ 8.2   │ 5.4   │ Running   │ user     │ python3 app.py  │
│ 3456   │ systemd        │ 2.1   │ 0.8   │ Running   │ root     │ /sbin/systemd   │
└─────────────────────────────────────────────────────────────────────────────────┘

🚨 Alerts: CPU usage high (85.2% > 80%) | 📊 Uptime: 2d 14h 32m | ⚡ Load: 2.1/8.0
Last updated: 2024-01-15 14:30:25 | Press 'q' to quit, 'r' to refresh, 'h' for help
```

### System Health Report

```
📊 System Health Report - Generated 2024-01-15 14:30:25

┌─────────────────────────────────────────────────────────────────────────────────┐
│ System Information                                                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│ OS: CachyOS Linux x86_64                    Kernel: 6.6.10-1-cachyos           │
│ CPU: AMD Ryzen 7 5800X (16) @ 3.800GHz     GPU: NVIDIA GeForce RTX 3080        │
│ Memory: 16384 MB                            Storage: 1TB NVMe SSD               │
│ Uptime: 2 days, 14 hours, 32 minutes       Load Average: 2.1, 1.8, 1.5        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ Performance Metrics (Last 24 Hours)                                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│ CPU Usage:    Average: 45.2% | Peak: 89.1% | Low: 12.4%                      │
│ Memory Usage: Average: 68.5% | Peak: 84.2% | Low: 45.1%                      │
│ Disk I/O:     Read: 2.1 GB/h | Write: 890 MB/h | IOPS: 1.2K                  │
│ Network:      Download: 45.2 GB | Upload: 12.8 GB | Peak: 180 MB/s           │
│ Temperature:  CPU Avg: 55°C | CPU Peak: 72°C | GPU Avg: 48°C                 │
└─────────────────────────────────────────────────────────────────────────────────┘

✅ System Status: HEALTHY
🚨 Warnings: CPU temperature peaked at 72°C (consider better cooling)
💡 Recommendations: Consider upgrading RAM for better performance
```

## ⚙️ Configuration

Configuration is stored at `~/.config/health-dashboard/config.json`:

```json
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
    "log_path": "~/.local/share/health-dashboard/logs/"
  },
  "display": {
    "show_processes": true,
    "process_count": 10,
    "show_network": true,
    "show_temperatures": true,
    "show_disk_io": true,
    "colored_output": true
  }
}
```

## 🔧 Requirements

- **Python 3.7+**
- **Virtual environment** (automatically created)
- **Linux/macOS/Windows** (optimized for Linux)

### Dependencies

```
psutil>=5.8.0          # System information
rich>=12.0.0           # Beautiful terminal output
click>=8.0.0           # CLI interface
flask>=2.0.0           # Web dashboard
plotly>=5.0.0          # Interactive charts
schedule>=1.1.0        # Task scheduling
requests>=2.25.0       # HTTP requests
pynvml>=11.0.0         # NVIDIA GPU monitoring
```

### Optional Dependencies

```
# For advanced features
nvidia-ml-py3          # NVIDIA GPU detailed stats
py-cpuinfo            # Detailed CPU information
distro                # Linux distribution detection
```

## 🌡️ Temperature Monitoring

### Supported Sensors

- **CPU**: Core temperatures via thermal zones
- **GPU**: NVIDIA (via nvidia-ml) and AMD (via sysfs)
- **Motherboard**: System sensors via lm-sensors
- **Storage**: NVMe and SATA drive temperatures
- **Custom**: User-defined sensor paths

### Thermal Management

- **Throttling Detection**: Automatic detection of thermal throttling
- **Fan Control**: Integration with system fan controls
- **Alerts**: Temperature-based warnings and critical alerts
- **Trends**: Historical temperature tracking and analysis

## 🌐 Web Dashboard

### Features

- **Real-time Updates**: WebSocket-based live data
- **Interactive Charts**: Plotly-powered visualizations
- **Mobile Responsive**: Works on phones and tablets
- **Dark/Light Themes**: Multiple UI themes
- **Multi-system**: Monitor multiple systems from one dashboard

### API Endpoints

```
GET /api/system          # Current system stats
GET /api/processes       # Running processes
GET /api/history         # Historical data
GET /api/alerts          # Active alerts
POST /api/alerts/config  # Update alert configuration
```

## 🚀 Performance Optimization

### CachyOS Specific Features

- **Kernel Optimization Detection**: Detects CachyOS performance kernels
- **CPU Governor Monitoring**: Tracks performance/powersave modes
- **Memory Optimization**: CachyOS-specific memory tuning detection
- **I/O Scheduler**: Monitors and suggests optimal I/O schedulers

### System Tuning Suggestions

- **CPU Frequency Scaling**: Recommendations for performance
- **Memory Management**: Swap and cache optimization tips
- **Disk Performance**: I/O scheduler and mount option suggestions
- **Network Tuning**: TCP/UDP optimization recommendations

## 🛠️ Development

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run directly
python3 health_dashboard.py --help
```

### Project Structure

```
system-health-dashboard/
├── health_dashboard.py       # Main application
├── web/                      # Web dashboard files
│   ├── app.py               # Flask web application
│   ├── static/              # CSS, JS, images
│   └── templates/           # HTML templates
├── install_venv.sh          # Virtual environment installer
├── run.sh                   # Runner script
├── requirements.txt         # Dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
└── tests/                  # Test suite
    ├── test_monitoring.py
    ├── test_alerts.py
    └── test_web.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [psutil](https://github.com/giampaolo/psutil) for cross-platform system information
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- [Flask](https://flask.palletsprojects.com/) for the web dashboard
- [Plotly](https://plotly.com/python/) for interactive charts

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/LinuxCTRL/system-health-dashboard/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/LinuxCTRL/system-health-dashboard/discussions)
- 📧 **Contact**: [sofalcons@outlook.com](mailto:sofalcons@outlook.com)

---

⭐ **Star this repo** if it helps you monitor your system!

**Made with ❤️ by LinuxCTRL - Controlling the world through better developer tools!** 🌍💪

_Part of the LinuxCTRL Developer Toolkit - Building tools that developers actually want to use._

**Optimized for CachyOS and performance enthusiasts!** 🐧⚡
