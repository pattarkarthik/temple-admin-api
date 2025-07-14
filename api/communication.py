from twilio.rest import Client
from dotenv import load_dotenv
import requests
import os

load_dotenv()

def send_message(numbers, message):
    print("whatsapp url "+os.getenv("WHATSAPP_API_URL"))
    for number in numbers:
        headers = {
            "Authorization":  os.getenv("WHATSAPP_ACCESS_TOKEN")}
        payload= {"messaging_product":"whatsapp",
                    "recipient_type": "individual",
                    "to": number, 
                    "type":"text",
                    "text":{"body":message}
                    }
            
        response=requests.post(os.getenv("WHATSAPP_API_URL"),headers=headers,json=payload)
        print(response)
        # reponse_data=response.json()
        
   