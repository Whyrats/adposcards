from telethon import TelegramClient, events
import os
from utils.file_processor import process_file

api_id = os.getenv('20256610')
api_hash = os.getenv('c9d1a29639f4b852a1ff45dd8fc1f380')
bot_token = os.getenv('7018525368:AAFh8P9kZ4eNcFAswTdE1Ec6nz7we1NnwFo')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Привет! Пожалуйста, загрузите .xlsx файл с данными.')
    raise events.StopPropagation

@client.on(events.NewMessage)
async def handle_file(event):
    if event.message.file:
        file_path = await event.message.download_media()
        if file_path.endswith('.xlsx'):
            results = process_file(file_path)
            response = "\n".join([f"`{result}`" for result in results])
            await event.respond(response, parse_mode='markdown')
            os.remove(file_path)
        else:
            await event.respond('Пожалуйста, загрузите файл в формате .xlsx.')
    else:
        await event.respond('Пожалуйста, загрузите .xlsx файл с данными.')

def main():
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
