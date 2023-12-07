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
