from dotenv import load_dotenv
import os
import requests
from fastapi import FastAPI, Request

# Load .env.local file
load_dotenv('.env.local')

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Home, use /message/ api to send message to slack"}

@app.get("/message/") 
async def get_message(request: Request):
    query_params = request.query_params
    text = query_params.get('text')
    response = send_text_message(text)
    return {"query_params": query_params,"response": response}

def send_text_message(message=''):   
    # Access environment variables
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    if WEBHOOK_URL is None:
        return "Failed to load WEBHOOK_URL env variable."
    # Define the URL and payload
    payload = {"text": "Message: "+message}

    # Send the POST request
    response = requests.post(WEBHOOK_URL, json=payload)

    # Check the response
    if response.status_code == 200:
        return ("Message sent successfully!")
    else:
        return f"Failed to send message. Status code: {response.status_code}, Response: {response.text}"
