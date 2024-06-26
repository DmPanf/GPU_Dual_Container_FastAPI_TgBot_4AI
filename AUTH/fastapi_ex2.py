# fastapi_ex2.py

from fastapi import FastAPI, Request
import GPUtil
import psutil

app = FastAPI()

@app.get("/info")
async def read_root(request: Request):
    client_ip = request.client.host

    # Получение информации о GPU
    gpus = GPUtil.getGPUs()
    gpu_info = [{'name': gpu.name, 'load': gpu.load, 'free_memory': gpu.memoryFree, 'total_memory': gpu.memoryTotal, 'temperature': gpu.temperature} for gpu in gpus]

    # Получение информации о RAM
    ram = psutil.virtual_memory()
    ram_info = {'total': ram.total, 'available': ram.available, 'used': ram.used, 'percent': ram.percent}

    return {
        'Project 2023': 'Pothole Detection [Moscow, 2023 г.]',
        'Client IP': client_ip,
        'GPU Info': gpu_info,
        'RAM Info': ram_info
    }
