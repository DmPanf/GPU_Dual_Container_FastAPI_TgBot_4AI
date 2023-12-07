Для реализации функционала, который вы описали в FastAPI, вам нужно выполнить несколько шагов:

1. Чтение списка режимов и активного режима из `.env` файла.
2. Вывод списка режимов через API, подсветив активный.
3. Предоставление возможности выбора нового режима через API.
4. Обновление `.env` файла с новым выбранным режимом.

Однако, стоит отметить, что изменение `.env` файла в рантайме не является типичной или рекомендуемой практикой. Файл `.env` обычно используется для инициализации настроек при запуске приложения, и не предназначен для динамического обновления во время выполнения. Вместо этого, лучше использовать базу данных или другое средство хранения для управления изменяемыми настройками.

Тем не менее, если вы все же хотите реализовать это через `.env` файл, вот примерный подход:

### Шаг 1: Установка зависимостей

Убедитесь, что у вас установлены `fastapi`, `uvicorn` и `python-dotenv`:

```bash
pip install fastapi uvicorn python-dotenv
```

### Шаг 2: Код FastAPI приложения

```python
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv, set_key
from pathlib import Path
import os

app = FastAPI()
load_dotenv()

ENV_FILE = '.env'

@app.get("/modes")
def get_modes():
    modes = os.getenv("Modes_List", "").split(',')
    active_mode = os.getenv("Active_Mode")
    return {"modes": modes, "active_mode": active_mode}

@app.post("/modes/{mode}")
def set_mode(mode: str):
    modes = os.getenv("Modes_List", "").split(',')
    if mode not in modes:
        raise HTTPException(status_code=400, detail="Invalid mode")

    # Обновляем .env файл (не рекомендуется для продакшена)
    env_path = Path(ENV_FILE)
    set_key(env_path, "Active_Mode", mode)
    return {"success": True, "active_mode": mode}
```

### Пример .env файла

```
Modes_List=mode1,mode2,mode3
Active_Mode=mode1
```

### Запуск сервера

```bash
uvicorn main:app --reload
```

### Важные замечания

1. **Безопасность**: Ваш API позволяет клиенту выбрать режим из предопределенного списка. Убедитесь, что это не приведет к нежелательным последствиям.

2. **Обновление .env**: Метод `set_key` из библиотеки `python-dotenv` физически перезапишет файл `.env`. Это может быть не лучшая практика, особенно в продакшене, где изменения конфигурации обычно управляются через CI/CD пайплайны или конфигурационные системы.

3. **Перезапуск приложения**: FastAPI само по себе не будет автоматически перезагружать переменные окружения после их изменения в `.env` файле. Для применения изменений может потребоваться перезапуск приложения.
