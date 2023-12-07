Для динамического управления конфигурацией в вашем приложении FastAPI лучше использовать альтернативные подходы, не связанные с файлом `.env`. `.env` файлы обычно используются для начальной конфигурации и не предназначены для изменений во время работы приложения. Вот несколько рекомендуемых подходов:

### 1. Внутреннее хранилище состояния

Вы можете использовать внутреннее хранилище в вашем приложении для сохранения и изменения состояний. Это может быть простой глобальный объект или более сложная структура, в зависимости от ваших потребностей.

```python
from fastapi import FastAPI

app = FastAPI()
app.state.modes = ["mode1", "mode2", "mode3"]
app.state.active_mode = "mode1"

@app.get("/modes")
def get_modes():
    return {"modes": app.state.modes, "active_mode": app.state.active_mode}

@app.post("/modes/{mode}")
def set_mode(mode: str):
    if mode not in app.state.modes:
        return {"error": "Invalid mode"}
    app.state.active_mode = mode
    return {"active_mode": app.state.active_mode}
```

### 2. База данных

Если ваше приложение уже работает с базой данных, вы можете использовать ее для хранения и изменения конфигурационных параметров.

```python
# Предполагается, что у вас уже есть настроенная база данных
@app.post("/modes/{mode}")
def set_mode(mode: str, db: Session = Depends(get_db)):
    if mode not in get_modes_from_db(db):
        raise HTTPException(status_code=400, detail="Invalid mode")
    set_active_mode_in_db(db, mode)
    return {"active_mode": mode}
```

### 3. Кэширование

Для высоконагруженных систем или систем с распределенной архитектурой вы можете использовать решения для кэширования, такие как Redis, для хранения и быстрого доступа к конфигурационным параметрам.

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.post("/modes/{mode}")
def set_mode(mode: str):
    if mode not in redis_client.lrange("modes", 0, -1):
        raise HTTPException(status_code=400, detail="Invalid mode")
    redis_client.set("active_mode", mode)
    return {"active_mode": mode}
```

### 4. Файл конфигурации

Если вам действительно нужно сохранять конфигурацию в файле, лучше использовать специализированные форматы файлов конфигурации, такие как JSON или YAML, и писать в них при помощи соответствующих библиотек.

### Важные соображения

- **Безопасность**: Убедитесь, что ваш API защищен, особенно если вы позволяете изменять конфигурацию через него.
- **Отказоустойчивость**: При использовании внешних хранилищ данных (как баз данных или кэшей) убедитесь, что ваше приложение может корректно обрабатывать потерю соединения с ними.
- **Производительность**: При выборе метода управления конфигурацией учитывайте его влияние на производительность вашего приложения.
