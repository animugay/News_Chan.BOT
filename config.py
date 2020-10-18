import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

url_ongoing = os.getenv("URL_ONGOING")
url_news = os.getenv("URL_NEWS")

admin_id = os.getenv("admin_id")

