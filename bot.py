from telethon import TelegramClient, events, Button
import os
from utils.file_processor import process_file
from database import init_db, set_export_format, get_export_format
from xlsx_exporter import create_xlsx_file

# Загружаем переменные окружения
api_id = os.getenv('YOUR_API_ID')
api_hash = os.getenv('YOUR_API_HASH')
bot_token = os.getenv('BOT_TOKEN')

print(f"API_ID: {api_id}, API_HASH: {api_hash}, BOT_TOKEN: {bot_token}")

# Создаем клиента Telegram
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Инициализируем базу данных
init_db()

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    print("/start command received")
    await event.respond('Привет! Пожалуйста, загрузите .xlsx файл с данными 📄 или используйте /settings для настройки формата экспорта.')
    raise events.StopPropagation

@client.on(events.NewMessage(pattern='/settings'))
async def settings(event):
    print("/settings command received")
    buttons = [
        [Button.inline("Экспорт в .txt 📄", b'txt')],
        [Button.inline("Экспорт в .xlsx 📊", b'xlsx')]
    ]
    await event.respond('Выберите формат экспорта:', buttons=buttons)
    raise events.StopPropagation

@client.on(events.CallbackQuery)
async def callback(event):
    user_id = event.sender_id
    data = event.data.decode('utf-8')
    print(f"Callback received: {data}")

    if data in ['txt', 'xlsx']:
        set_export_format(user_id, data)
        await event.respond(f'Формат экспорта установлен на {data}.')
        await event.delete()

@client.on(events.NewMessage)
async def handle_file(event):
    print("New message received")
    if event.message.file:
        file_path = await event.message.download_media()
        print(f"File downloaded to: {file_path}")
        if file_path.endswith('.xlsx'):
            try:
                user_id = event.sender_id
                export_format = get_export_format(user_id)
                processed_data = process_file(file_path)
                if export_format == 'txt':
                    txt_file_path = "AdposCards.txt"
                    with open(txt_file_path, 'w') as txt_file:
                        txt_file.write('\n'.join(processed_data))
                    await event.respond('Файл успешно обработан и сохранен в формате .txt 📄.')
                    # Отправка файла обратно пользователю
                    await client.send_file(event.chat_id, txt_file_path)
                    # Отправка обработанных данных в сообщении
                    message_text = '\n'.join([f'{i+1}. `{card}`' for i, card in enumerate(processed_data)])
                    await event.respond(message_text, parse_mode='markdown')
                elif export_format == 'xlsx':
                    xlsx_file_path = "AdposCards.processed.xlsx"
                    create_xlsx_file(processed_data, xlsx_file_path)
                    await event.respond('Файл успешно обработан и сохранен в формате .xlsx 📊.')
                    # Отправка файла обратно пользователю
                    await client.send_file(event.chat_id, xlsx_file_path)
                    # Отправка обработанных данных в сообщении
                    message_text = '\n'.join([f'{i+1}. `{card}`' for i, card in enumerate(processed_data)])
                    await event.respond(message_text, parse_mode='markdown')
            except Exception as e:
                print(f"Error processing file: {e}")
                await event.respond(f'Произошла ошибка при обработке файла: {e}')
        else:
            await event.respond('Пожалуйста, загрузите .xlsx файл.')

if __name__ == '__main__':
    print("Starting bot...")
    client.run_until_disconnected()
