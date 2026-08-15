import os
import time
import psutil


def get_process_usage():
    process = psutil.Process(os.getpid())

    return {
        "process_cpu_percent": process.cpu_percent(interval=0.1),
        "process_memory_mb": (
            process.memory_info().rss / (1024 * 1024)
        ),
    }


def get_system_usage():
    return {
        "system_cpu_percent": psutil.cpu_percent(interval=0.1),
        "system_memory_percent": psutil.virtual_memory().percent,
    }


def monitor_for(seconds=10, interval=1):
    samples = []

    end_time = time.time() + seconds

    while time.time() < end_time:

        process = get_process_usage()
        system = get_system_usage()

        samples.append({
            **process,
            **system,
        })

        time.sleep(interval)

    return samples