# Dockerfile for YOLOv8
# официальный базовый образ TensorFlow GPU Jupyter
FROM tensorflow/tensorflow:latest-gpu-jupyter

# Установка необходимых пакетов и обновление системы
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx && \
    pip install --no-cache-dir -U pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip with no cache # Один RUN лучше, чем множество RUN команд для уменьшения количества слоев в Docker-образе
# RUN pip install --no-cache-dir -U pip

# рабочая директория в контейнере
WORKDIR /app

# Копирование файлов в рабочую директорию
COPY . /app/

# Установка дополнительных зависимостей, указанных в requirements.txt (если они есть)
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

EXPOSE 8001

# Запуск FastAPI на порту 8001 на 0.0.0.0 (по умолчанию) и слушать на этом порту
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
