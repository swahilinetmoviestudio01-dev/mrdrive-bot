import os
import json
import telebot
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Tunachukua Token kwa siri kutoka Render bila mtu kuiona GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Tunachukua siri za Google Drive kutoka Render kwa usalama
google_json_secrets = os.getenv("GOOGLE_DRIVE_JSON")
info = json.loads(google_json_secrets)

SCOPES = ['https://googleapis.com']
creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Habari! Mimi ni Drive Robot wako. Nitumie neno: /unda Jina_La_Folda")

@bot.message_handler(commands=['unda'])
def create_folder(message):
    try:
        jina_la_folda = message.text.replace('/unda ', '').strip()
        if not jina_la_folda or jina_la_folda == '/unda':
            bot.reply_to(message, "Tafadhali andika jina la folda. Mfano: `/unda Movies`")
            return

        file_metadata = {
            'name': jina_la_folda,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
        bot.reply_to(message, f"✅ Folda '{jina_la_folda}' imeundwa kwenye Google Drive!\nID yake ni: {folder.get('id')}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hitilafu imetokea: {str(e)}")

print("Roboti inafanya kazi...")
bot.infinity_polling()
      
