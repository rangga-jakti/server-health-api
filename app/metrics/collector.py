import psutil

def get_cpu():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
    }

def get_ram():
    ram = psutil.virtual_memory()
    return {
        "total": ram.total,
        "available": ram.available,
        "used": ram.used,
        "ram_percent": ram.percent
    }

def get_disk():
    disk = psutil.disk_usage("/")
    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "disk_percent": disk.percent
    }

def get_processes():
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            pass
    return sorted(processes, key=lambda x: x["cpu_percent"] or 0, reverse=True)[:10]

def get_summary():
    return {
        "cpu": get_cpu(),
        "ram": get_ram(),
        "disk": get_disk()
    }