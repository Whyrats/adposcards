from telethon import TelegramClient, events
import os
from utils.file_processor import process_file

api_id = os.getenv('YOUR_API_ID')
api_hash = os.getenv('YOUR_API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Привет! Пожалуйста, загрузите .xlsx файл с данными 📄.')
    raise events.StopPropagation

@client.on(events.NewMessage)
async def handle_file(event):
    if event.message.file:
        file_path = await event.message.download_media()
        if file_path.endswith('.xlsx'):
            try:
                results = process_file(file_path)
                response = "\n".join([f"{index + 1}. `{result}`" for index, result in enumerate(results)])
                
                # Создание .txt файла
                txt_file_path = 'AdposCards.txt'
                with open(txt_file_path, 'w') as f:
                    for index, result in enumerate(results):
                        f.write(f"{index + 1}. {result}\n")
                
                await event.respond(response, parse_mode='markdown')
                await event.respond('Вот ваш файл с результатами 📄:')
                await event.respond(file=txt_file_path)
                
                os.remove(file_path)
                os.remove(txt_file_path)
            except Exception as e:
                await event.respond(f'Произошла ошибка при обработке файла: {str(e)} ❌')
        else:
            await event.respond('Пожалуйста, загрузите файл в формате .xlsx ❗.')
    else:
        await event.respond('Пожалуйста, загрузите .xlsx файл с данными 📄.')

def main():
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
