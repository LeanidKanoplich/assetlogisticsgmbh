import requests
import config

TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url, json=payload)
    return response.json()

def send_audio(chat_id, audio_url, caption=None):
    url = f"{TELEGRAM_API_URL}/sendAudio"
    payload = {
        'chat_id': chat_id,
        'audio': audio_url,
        'caption': caption,
    }
    response = requests.post(url, json=payload)
    return response.json()

def set_webhook(url):
    webhook_url = f"{TELEGRAM_API_URL}/setWebhook?url={url}"
    response = requests.get(webhook_url)
    return response.json()

def get_file_path(file_id):
    url = f"{TELEGRAM_API_URL}/getFile?file_id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        file_path = response.json()['result']['file_path']
        return {"status": 1, "file_path": file_path}
    return {"status": 0, "message": "Failed to get file path"}

def save_file_and_get_local_path(file_path):
    file_url = f"https://api.telegram.org/file/bot{config.TOKEN}/{file_path}"
    local_file_path = f"/tmp/{file_path.split('/')[-1]}"
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as f:
            f.write(response.content)
        return {"status": 1, "local_file_path": local_file_path, "file_id": file_path.split('/')[-1]}
    return {"status": 0, "message": "Failed to save file"}
