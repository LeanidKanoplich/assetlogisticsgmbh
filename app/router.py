from fastapi import APIRouter, Request, UploadFile, File
from openai_apis import text_to_speech, transcript_audio, chat_completion
from telegram_api import send_audio, send_message, set_webhook, get_file_path, save_file_and_get_local_path
from utils import upload_file_to_gcs
import config

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    temp_file_path = f"/tmp/{file.filename}"
    
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())
    
    public_url = upload_file_to_gcs(temp_file_path, file.filename)
    
    if public_url:
        return {"file_url": public_url}
    else:
        return {"error": "Failed to upload file"}

@router.post('/telegram')
async def telegram(request: Request):
    try:
        body = await request.json()
        print(body)
        sender_id = body['message']['from']['id']
        if 'voice' in body['message'].keys():
            file_id = body['message']['voice']['file_id']
            file_path = get_file_path(file_id)
            if file_path['status'] == 1:
                local_file_path = save_file_and_get_local_path(
                    file_path['file_path'])
                if local_file_path['status'] == 1:
                    transcript = transcript_audio(
                        local_file_path['local_file_path'], local_file_path['file_id'])
                    if transcript['status'] == 1:
                        query = chat_completion(transcript['transcript'])
        else:
            query = body['message']['text']
        response = chat_completion(query)
        if config.REPLY_TYPE == 'audio':
            audio_file_path, audio_file_name = text_to_speech(response)
            public_url = upload_file_to_gcs(audio_file_path, audio_file_name)
            send_audio(sender_id, public_url, 'Response')
        else:
            send_message(sender_id, response)
        return 'OK', 200
    except Exception as e:
        print('Error at telegram...')
        print(e)
        return 'OK', 200
    
{
"secret_token": "2f6OpVEPB9nnhYLvrvgEWUp6fMy_3eNqobLfoSiapSgRSR73r",
"url": "https://d6580e3daa72.ngrok.app/telegram"
}

@router.get('/set-telegram-webhook')
async def set_telegram_webhook(request: Request):
    try:
        base_url = str(request.base_url)
        webhook_url = f"{base_url}telegram"
        set_webhook(webhook_url)
        return "OK", 200
    except Exception as e:
        print('Error at set_telegram_webhook...')
        print(e)
        return 'BAD REQUEST', 400
