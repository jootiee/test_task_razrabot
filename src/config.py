from os import getenv
from dotenv import load_dotenv

load_dotenv()


proxies = {"http":      getenv("HTTP_PROXY"),
           "https":     getenv("HTTPS_PROXY")
           }

BOT_TOKEN = getenv("BOT_TOKEN")