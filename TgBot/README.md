# Simple TgBot Documentation

This repository contains a simple Telegram bot implemented using the `aiogram` library. The bot has various functionalities including fetching information, processing images, and more. Below is a detailed guide on how to set up and run the bot.

## Table of Contents
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Installation](#installation)
- [Bot Functionality](#bot-functionality)
  - [Commands](#commands)
  - [Image Processing](#image-processing)
- [Logging](#logging)
- [Running the Bot](#running-the-bot)

## Setup

### Prerequisites
Before running the bot, ensure you have the following installed:
- Python 3.7 or higher
- `aiogram` library
- `aiohttp` library
- `python-dotenv` library

### Environment Variables
Create a `.env` file in the root directory of your project and add the following environment variables:

```ini
TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
CHAT_ID=<YOUR_ADMIN_CHAT_ID>
API_URL=<YOUR_API_URL>
mdl_name=<YOUR_MODEL_NAME>
LOG_DIR=<DIRECTORY_FOR_LOGS>
LOG_FILE=<LOG_FILE_NAME>
```

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/simple-bot.git
   cd simple-bot
   ```
2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

## Bot Functionality

### Commands
The bot supports the following commands:

- `/start` or `/info`: Fetches and sends project information from the server.
- `/help`: Sends a help message with instructions.

### Image Processing
The bot can process images sent by users. When an image is received, it is sent to a FastAPI server for processing. The server returns the processed image and additional information which is then sent back to the user.

### Logging
Logs are stored in the directory specified by the `LOG_DIR` environment variable. Log files are named according to the `LOG_FILE` environment variable.

## Running the Bot
To run the bot, execute the following command:

```sh
python bot.py
```

## Code Overview

### bot.py
This file contains the main logic for the Telegram bot. Below is a brief overview of its contents:

#### Imports and Environment Setup

```python
from aiogram import Bot, Dispatcher, types
import logging
import asyncio
import aiohttp
from aiohttp import ClientTimeout
import json
from dotenv import load_dotenv
from io import BytesIO
import base64
import os
import csv
from datetime import datetime
from text_module import commands, help_text

load_dotenv()
API_TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
API_URL = os.getenv("API_URL")
mdl_name = os.getenv("mdl_name")
log_folder = os.getenv("LOG_DIR")
log_file = os.getenv("LOG_FILE")
```

#### Logging Configuration

```python
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"{log_folder}/{log_file}"),
        logging.StreamHandler()
    ]
)
```

#### Bot Initialization

```python
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
```

#### Handlers and Functions

**Startup Message:**

```python
async def on_startup(dp):
    bot_info = await dp.bot.get_me()
    bot_name = bot_info.username
    await dp.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f'✴️ Бот @{bot_name} запущен!')
```

**Fetching Data:**

```python
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")
    except Exception as e:
        logging.error(f"fetch ------ Error occurred: {e}")
        raise e
```

**Saving to CSV:**

```python
def save_to_csv(results, user_id, user_name, phone):
    with open('./data/save_images.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), user_id, user_name, phone, *results.values()])
```

**Command Handlers:**

```python
@dp.message_handler(commands=['start', 'info'])
async def send_info(message: types.Message):
    timeout = ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            info = await fetch(session, f'{API_URL}/info') 
            data = json.loads(info)["Project 2023"]
            await message.answer(f"🔰 <b>Project Info:</b>\n<pre>{data}</pre>", parse_mode="HTML")
        except Exception as e:
            logging.error(f"info ------ Error occurred: {e}")
            await message.answer(f"⛔️ Сервер <b>FastAPI</b> недоступен!\n{e}", parse_mode="HTML")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer(help_text, parse_mode="Markdown")
```

**Image Processing:**

```python
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_image(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    image_data = await bot.download_file(file_path)
    url = f'{API_URL}/predict'

    timeout = ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        form = aiohttp.FormData()
        form.add_field('file', image_data, filename='input_image.jpg', content_type='image/jpg')
        form.add_field('mdl_name', mdl_name)
        try:
            async with session.post(url, data=form) as response:
                if response.status == 200:
                    response_json = await response.json()
                    img_str = response_json['image']
                    results = response_json['results']

                    add_info = f"\n<b>📟 Показание прибора:</b> [<code>{results['counter']}</code>]" \
                               f"\n<b>⏱ Время обработки:</b> {results['inference']}ms" \
                               f"\n<b>⚖️ Модель:</b> {results['model_name']}" \
                               f"\n<b>🔍 Распознано {results['object_count']} объектов</b>" \
                               f"\n<b>📆 Дата/Время:</b> <code>{results['current_time']}</code>" \
                               f"\n<b>📸 Изображение {results['wh_check']}</b>" \
                               f"\n<b>💾 Имя файла:</b> <code>{results['file_name']}</code>"
                    
                    user_id = message.from_user.id
                    user_name = message.from_user.username
                    phone = message.contact.phone_number if message.contact else 'N/A'
                    save_to_csv(results, user_id, user_name, phone)

                    output_image_data = BytesIO(base64.b64decode(img_str))
                    output_image_data.seek(0)
                    await message.reply_photo(photo=output_image_data, caption=add_info, parse_mode="HTML")
        except KeyError as key_error:
            logging.error(f"Key error: {key_error}")
            await message.answer(f"🛑 Ошибка обработки: {key_error}")
        except Exception as e:
            logging.error(f"predict ------ ⛔️ Сервер недоступен: {e}")
            await message.answer(f"⛔️ Сервер <b>FastAPI [{API_URL}]</b> недоступен!\n⌛️ Timeout=<b>{timeout} s</b>\n{e}", parse_mode="HTML")
```

### Main Function

```python
async def main():
    await on_startup(dp)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
```
