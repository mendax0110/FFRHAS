import os
import time
import subprocess
import psutil
import platform
import socket

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)
except ImportError:
    GPIO = None

def check_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = int(f.read()) / 1000
        return {"cpu_temp": temp, "ok": temp < 85}
    except Exception as e:
        return {"cpu_temp": None, "error": str(e)}

def check_cpu_usage():
    usage = psutil.cpu_percent(interval=1)
    return {"cpu_usage": usage, "ok": usage < 95}

def check_disk():
    usage = psutil.disk_usage('/')
    return {"disk_usage": usage.percent, "ok": usage.percent < 90}

def check_memory():
    mem = psutil.virtual_memory()
    return {"memory_usage": mem.percent, "ok": mem.percent < 90}

def check_uptime():
    uptime = time.time() - psutil.boot_time()
    return {"uptime": uptime}

def check_network():
    try:
        subprocess.run(["ping", "-c", "1", "-W", "2", "8.8.8.8"], stdout=subprocess.DEVNULL)
        return {"network": True}
    except Exception:
        return {"network": False}

def check_gpio():
    if GPIO:
        try:
            state = GPIO.input(18)
            return {"gpio_18": state}
        except Exception as e:
            return {"gpio_18": None, "error": str(e)}
    return {"gpio_18": None, "error": "GPIO not available"}

def get_system_info():
    return {
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
        "cpu_cores": psutil.cpu_count(logical=True)
    }

def run_health_checks():
    return {
        "system": get_system_info(),
        "cpu_temp": check_cpu_temp(),
        "cpu_usage": check_cpu_usage(),
        "disk": check_disk(),
        "memory": check_memory(),
        "uptime": check_uptime(),
        "network": check_network(),
        "gpio": check_gpio()
    }