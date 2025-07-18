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
            },
            "display": {
                "show_processes": True,
                "process_count": 10
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
    """Launch real-time system dashboard"""
    
    console.print(Panel.fit("System Health Dashboard v1.0.0", style="bold blue"))
    
    if monitor.system_info['is_cachyos']:
        console.print("[bold green]CachyOS Performance System Detected![/bold green]")
    
    try:
        while True:
            console.clear()
            
            # Get current stats
            cpu_info = monitor.get_cpu_info()
            memory_info = monitor.get_memory_info()
            disk_info = monitor.get_disk_info()
            
            # Create main table
            table = Table(title="System Status")
            table.add_column("Component", style="cyan")
            table.add_column("Usage", style="green")
            table.add_column("Details", style="yellow")
            
            # CPU row
            cpu_details = f"Freq: {cpu_info['frequency']:.0f}MHz | Cores: {cpu_info['core_count']}"
            table.add_row("CPU", f"{cpu_info['usage_percent']:.1f}%", cpu_details)
            
            # Memory row
            mem_details = f"Used: {monitor.format_bytes(memory_info['used'])} / {monitor.format_bytes(memory_info['total'])}"
            table.add_row("Memory", f"{memory_info['percent']:.1f}%", mem_details)
            
            # Disk rows
            for disk in disk_info[:3]:
                disk_details = f"Free: {monitor.format_bytes(disk['free'])}"
                table.add_row(f"Disk ({disk['mountpoint']})", f"{disk['percent']:.1f}%", disk_details)
            
            console.print(table)
            
            # Show top processes if detailed
            if detailed:
                processes = monitor.get_top_processes(5)
                proc_table = Table(title="Top Processes")
                proc_table.add_column("PID", style="cyan")
                proc_table.add_column("Name", style="green")
                proc_table.add_column("CPU%", style="yellow")
                proc_table.add_column("Memory%", style="red")
                
                for proc in processes:
                    proc_table.add_row(
                        str(proc['pid']),
                        proc['name'][:20],
                        f"{proc['cpu_percent']:.1f}",
                        f"{proc['memory_percent']:.1f}"
                    )
                
                console.print(proc_table)
            
            # Show system info
            uptime = monitor.format_uptime(monitor.system_info['boot_time'])
            load_avg = cpu_info['load_avg'][0]
            info_text = f"Uptime: {uptime} | Load: {load_avg:.2f}"
            
            console.print(f"\n[dim]{info_text}[/dim]")
            console.print("[dim]Press Ctrl+C to exit[/dim]")
            
            time.sleep(2)
            
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