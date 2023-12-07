Чтобы перенести данные о `Active_Mode` и `Modes_List` из файла `.env` в файл `config.json`, вам нужно будет преобразовать их в соответствующий JSON формат и затем обновить логику работы с конфигурацией в вашем FastAPI приложении. Вот шаги, которые вам нужно выполнить:

### Шаг 1: Обновление файла config.json

Добавьте новые поля в ваш `config.json`, чтобы он выглядел примерно так:

```json
{
    "servers": [
        {
            "name": "SERVER-1 [docker LAN app:8001]",
            "url": "http://app:8001"
        },
        {
            "name": "SERVER-3 [localhost:8001]",
            "url": "http://localhost:8001"
        },
        {
            "name": "SERVER-4 [Private LAN]",
            "url": "http://10.10.7.204:8001"
        },
        {
            "name": "SERVER-4 [Private WAN]",
            "url": "http://81.90.3.17:8001"
        }
    ],
    "Active_Mode": "Basic",
    "Modes_List": ["Basic", "Grid", "HQ-SAM", "YOLOv8"]
}
```

### Шаг 2: Чтение и обработка файла config.json в FastAPI

В FastAPI приложении вы теперь будете читать настройки из `config.json` вместо `.env`.

```python
import json
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Функция для загрузки конфигурации
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

config = load_config()

@app.get("/modes")
def get_modes():
    return {
        "modes": config['Modes_List'], 
        "active_mode": config['Active_Mode']
    }

@app.post("/modes/{mode}")
def set_mode(mode: str):
    if mode not in config['Modes_List']:
        raise HTTPException(status_code=400, detail="Invalid mode")

    config['Active_Mode'] = mode

    # Сохранение изменений обратно в файл
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

    return {"active_mode": mode}
```

### Шаг 3: Работа с файлом config.json

Теперь, вся ваша конфигурация хранится в `config.json`, и вы можете обновлять `Active_Mode` через API. При этом изменения будут отражаться в файле `config.json`.

### Важные замечания

1. **Конкурентный доступ**: Если ваше приложение работает в среде с конкурентными запросами, нужно учитывать потенциальные проблемы с одновременной записью в файл.

2. **Безопасность**: Убедитесь, что ваш API и файл конфигурации должным образом защищены, особенно если они содержат чувствительные данные.

3. **Кеширование конфигурации**: В зависимости от частоты запросов, может быть целесообразно кешировать конфигурацию в памяти и обновлять её при необходимости, чтобы не читать файл при каждом запросе.
