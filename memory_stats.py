# Script to obtain system utilization information to track RAM usage during stem separation

import psutil
from datetime import datetime

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

def log_memory_stats(filename="memory_stats.txt"):
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    
    stats = (
        f"Timestamp: {datetime.now()}\n"
        f"--- Memory ---\n"
        f"Total: {mem.total / (1024 ** 3):.2f} GB\n"
        f"Available: {mem.available / (1024 ** 3):.2f} GB\n"
        f"Used: {mem.used / (1024 ** 3):.2f} GB\n"
        f"Percent: {mem.percent}%\n"
        f"--- Swap ---\n"
        f"Total: {swap.total / (1024 ** 3):.2f} GB\n"
        f"Used: {swap.used / (1024 ** 3):.2f} GB\n"
        f"Free: {swap.free / (1024 ** 3):.2f} GB\n"
        f"Percent: {swap.percent}%\n"
        f"--- CPU ---\n"
        f"Cores: {cpu_count}\n"
        f"Usage: {cpu_percent}%\n"
    )

    if GPU_AVAILABLE:
        gpus = GPUtil.getGPUs()
        stats += "--- GPU ---\n"
        for gpu in gpus:
            stats += (
                f"GPU ID: {gpu.id}\n"
                f"Name: {gpu.name}\n"
                f"Memory Total: {gpu.memoryTotal} MB\n"
                f"Memory Used: {gpu.memoryUsed} MB\n"
                f"Memory Free: {gpu.memoryFree} MB\n"
                f"GPU Load: {gpu.load * 100:.1f}%\n"
                f"GPU Temp: {gpu.temperature} °C\n"
            )

    stats += "-" * 30 + "\n"

    with open(filename, "a") as f:
        f.write(stats)