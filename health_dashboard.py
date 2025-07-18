#!/usr/bin/env python3
"""
System Health Dashboard - Monitor your system like a PRO!
Real-time system monitoring with beautiful CLI interface.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
import click
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout

# Initialize rich console
console = Console()

class SystemMonitor:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'health-dashboard'
        self.data_dir = Path.home() / '.local' / 'share' / 'health-dashboard'
        self.config_file = self.config_dir / 'config.json'
        
        # Create directories
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self.config = self.load_config()
        
        # Get system info
        self.system_info = self.get_system_info()
    
    def load_config(self):
        """Load configuration from file or create default"""
        default_config = {
            "refresh_interval": 2,
            "alerts": {
                "cpu_threshold": 80,
                "ram_threshold": 85,
                "disk_threshold": 90
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Create default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        return default_config
    
    def get_system_info(self):
        """Get basic system information"""
        try:
            import platform
            
            # Detect CachyOS
            is_cachyos = False
            os_name = platform.system()
            try:
                with open('/etc/os-release', 'r') as f:
                    os_info = f.read()
                    if 'cachyos' in os_info.lower():
                        is_cachyos = True
                        os_name = "CachyOS Linux"
            except:
                pass
            
            return {
                'os': os_name,
                'kernel': platform.release(),
                'hostname': platform.node(),
                'cpu_count': psutil.cpu_count(),
                'total_memory': psutil.virtual_memory().total,
                'boot_time': datetime.fromtimestamp(psutil.boot_time()),
                'is_cachyos': is_cachyos
            }
        except:
            return {
                'os': 'Unknown',
                'kernel': 'Unknown',
                'hostname': 'localhost',
                'cpu_count': 1,
                'total_memory': 0,
                'boot_time': datetime.now(),
                'is_cachyos': False
            }
    
    def format_bytes(self, bytes_value):
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def format_uptime(self, boot_time):
        """Format uptime"""
        uptime = datetime.now() - boot_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def get_cpu_info(self):
        """Get CPU usage and information"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)
        
        return {
            'usage_percent': cpu_percent,
            'frequency': cpu_freq.current if cpu_freq else 0,
            'load_avg': load_avg,
            'core_count': psutil.cpu_count()
        }
    
    def get_memory_info(self):
        """Get memory usage information"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total': memory.total,
            'used': memory.used,
            'free': memory.free,
            'percent': memory.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percent': swap.percent
        }
    
    def get_disk_info(self):
        """Get disk usage information"""
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': (usage.used / usage.total) * 100
                })
            except (PermissionError, OSError):
                continue
        return disks
    
    def get_top_processes(self, limit=10):
        """Get top processes by CPU usage"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.info
                proc_info['cpu_percent'] = proc.cpu_percent()
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return processes[:limit]
    
    def create_progress_bar(self, percentage, width=30):
        """Create a visual progress bar"""
        filled = int(width * percentage / 100)
        bar = "#" * filled + "-" * (width - filled)
        
        # Color based on percentage
        if percentage < 50:
            color = "green"
        elif percentage < 80:
            color = "yellow"
        else:
            color = "red"
            
        return f"[{color}]{bar}[/{color}] {percentage:.1f}%"

# Initialize the monitor instance
monitor = SystemMonitor()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """System Health Dashboard - Monitor your system like a PRO!"""
    pass

@cli.command()
@click.option('--detailed', is_flag=True, help='Show detailed system information')
@click.option('--refresh', default='2s', help='Refresh interval')
def dashboard(detailed, refresh):
    """Launch real-time system dashboard with smooth updates"""
    
    def generate_dashboard():
        """Generate the dashboard layout"""
        # Header
        header = "System Health Dashboard"
        if monitor.system_info['is_cachyos']:
            header += " - CachyOS Linux"
        
        # Create main layout
        layout = Layout()
        layout.split_column(
            Layout(Panel.fit(header, style="bold blue"), name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        # Split main into sections
        if detailed:
            layout["main"].split_column(
                Layout(name="cpu_memory"),
                Layout(name="disk"),
                Layout(name="processes")
            )
        else:
            layout["main"].split_column(
                Layout(name="cpu_memory"),
                Layout(name="disk")
            )
        
        # Get all system info
        cpu_info = monitor.get_cpu_info()
        memory_info = monitor.get_memory_info()
        disk_info = monitor.get_disk_info()
        
        # CPU and Memory section
        cpu_memory_table = Table.grid(padding=2)
        cpu_memory_table.add_column()
        cpu_memory_table.add_column()
        
        # CPU section
        cpu_section = Table(title="CPU Usage", border_style="blue")
        cpu_section.add_column("Metric", style="cyan")
        cpu_section.add_column("Value", style="green")
        
        cpu_section.add_row("Usage", monitor.create_progress_bar(cpu_info['usage_percent']))
        cpu_section.add_row("Cores", f"{cpu_info['core_count']}")
        cpu_section.add_row("Frequency", f"{cpu_info['frequency']:.0f} MHz")
        cpu_section.add_row("Load", f"{cpu_info['load_avg'][0]:.2f}")
        
        # Memory section
        memory_section = Table(title="Memory Usage", border_style="blue")
        memory_section.add_column("Metric", style="cyan")
        memory_section.add_column("Value", style="green")
        
        memory_section.add_row("Usage", monitor.create_progress_bar(memory_info['percent']))
        memory_section.add_row("Used", f"{monitor.format_bytes(memory_info['used'])}")
        memory_section.add_row("Free", f"{monitor.format_bytes(memory_info['free'])}")
        memory_section.add_row("Total", f"{monitor.format_bytes(memory_info['total'])}")
        
        cpu_memory_table.add_row(cpu_section, memory_section)
        layout["cpu_memory"].update(cpu_memory_table)
        
        # Disk section
        disk_section = Table(title="Disk Usage", border_style="blue")
        disk_section.add_column("Mount", style="cyan")
        disk_section.add_column("Usage", style="green")
        disk_section.add_column("Free", style="yellow")
        
        for disk in disk_info[:3]:
            disk_section.add_row(
                disk['mountpoint'],
                monitor.create_progress_bar(disk['percent']),
                monitor.format_bytes(disk['free'])
            )
        
        layout["disk"].update(disk_section)
        
        # Top Processes section (if detailed)
        if detailed:
            processes = monitor.get_top_processes(5)
            proc_table = Table(title="Top Processes", border_style="blue")
            proc_table.add_column("PID", style="cyan")
            proc_table.add_column("Name", style="green")
            proc_table.add_column("CPU%", style="yellow")
            proc_table.add_column("RAM%", style="red")
            
            for proc in processes:
                proc_table.add_row(
                    str(proc['pid']),
                    proc['name'][:15],
                    f"{proc['cpu_percent']:.1f}",
                    f"{proc['memory_percent']:.1f}"
                )
            
            layout["processes"].update(proc_table)
        
        # Footer with alerts and info
        uptime = monitor.format_uptime(monitor.system_info['boot_time'])
        load_avg = cpu_info['load_avg'][0]
        
        # Check for alerts
        alerts = []
        if cpu_info['usage_percent'] > 80:
            alerts.append(f"CPU usage high ({cpu_info['usage_percent']:.1f}% > 80%)")
        if memory_info['percent'] > 85:
            alerts.append(f"Memory usage high ({memory_info['percent']:.1f}% > 85%)")
        
        alert_text = " | ".join(alerts) if alerts else "All systems normal"
        footer_text = f"Alerts: {alert_text} | Uptime: {uptime} | Load: {load_avg:.1f} | Updated: {datetime.now().strftime('%H:%M:%S')} | Press Ctrl+C to exit"
        
        layout["footer"].update(Panel(footer_text, style="dim"))
        
        return layout
    
    # Use Live display for smooth updates
    try:
        with Live(generate_dashboard(), refresh_per_second=0.5, screen=True) as live:
            while True:
                time.sleep(2)
                live.update(generate_dashboard())
                
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped[/yellow]")

@cli.command()
def status():
    """Show current system status"""
    
    console.print(Panel.fit("System Status", style="bold blue"))
    
    # Get system info
    cpu_info = monitor.get_cpu_info()
    memory_info = monitor.get_memory_info()
    disk_info = monitor.get_disk_info()
    
    # System info table
    sys_table = Table(title="System Information")
    sys_table.add_column("Metric", style="cyan")
    sys_table.add_column("Value", style="green")
    
    sys_table.add_row("Hostname", monitor.system_info['hostname'])
    sys_table.add_row("OS", monitor.system_info['os'])
    sys_table.add_row("Kernel", monitor.system_info['kernel'])
    sys_table.add_row("Uptime", monitor.format_uptime(monitor.system_info['boot_time']))
    
    if monitor.system_info['is_cachyos']:
        sys_table.add_row("Performance", "CachyOS Optimized")
    
    console.print(sys_table)
    
    # Performance table
    perf_table = Table(title="Performance Metrics")
    perf_table.add_column("Component", style="cyan")
    perf_table.add_column("Usage", style="green")
    perf_table.add_column("Details", style="yellow")
    
    perf_table.add_row("CPU", f"{cpu_info['usage_percent']:.1f}%", f"{cpu_info['frequency']:.0f} MHz")
    perf_table.add_row("Memory", f"{memory_info['percent']:.1f}%", monitor.format_bytes(memory_info['used']))
    perf_table.add_row("Load Average", f"{cpu_info['load_avg'][0]:.2f}", "1min average")
    
    console.print(perf_table)

if __name__ == '__main__':
    # Set default command to dashboard
    if len(sys.argv) == 1:
        sys.argv.append('dashboard')
    cli()