Чтобы добавить информацию о сервере, такую как IP-адрес клиента, характеристики GPU и RAM, при обращении к эндпоинту `/info` в вашем FastAPI приложении, вам потребуется использовать дополнительные библиотеки и функции для сбора этой информации.

Вот пример, как это можно сделать:

1. **Сбор IP-адреса клиента**:
   Используйте объект `Request` для получения IP-адреса клиента.

2. **Получение информации о GPU**:
   Можно использовать библиотеку `GPUtil` для получения информации о GPU.

3. **Получение информации о RAM**:
   Используйте библиотеку `psutil` для получения информации о RAM.

Сначала установите необходимые библиотеки:

```bash
pip install fastapi uvicorn gputil psutil
```

Затем вот пример кода для вашего FastAPI приложения:

```python
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
```

Этот код возвращает информацию о проекте, IP-адрес клиента, детали о каждой доступной GPU и общую информацию о RAM при обращении к эндпоинту `/info`.

Обратите внимание, что информация о GPU будет доступна только если на сервере установлены GPU и библиотека `GPUtil` может их обнаружить. В противном случае, список GPU будет пустым.
