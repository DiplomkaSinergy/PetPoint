# config.py
from dotenv import load_dotenv
import os

load_dotenv()

# Telegram API
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(admin_id) for admin_id in os.getenv('ADMIN_IDS', '').split(',') if admin_id.isdigit()]
# Database
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_HOST = os.getenv('MYSQL_HOST')
# Payments
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')