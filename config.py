import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CREDENTIALS = os.getenv('CREDENTIALS')
GCP_CLOUD_STORAGE_BUCKET_NAME = os.getenv('GCP_CLOUD_STORAGE_BUCKET_NAME')
CREDENTIALS_FILE_PATH = "/tmp/credentials.json"
REPLY_TYPE = os.getenv('REPLY_TYPE', 'text')
