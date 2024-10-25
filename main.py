from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv


from mistralai import Mistral

import nkeypass

import os

load_dotenv()

app = FastAPI()

origins = ['http://localhost:3000', 
            'https://localhost:3000', 
           'https://localhost:8001', 
           'http://localhost:8080',
           'http://127.0.0.1',
           ]


# middleware
app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create a Mistral client instance
mistral_client = Mistral(
    api_key=os.environ["MISTRAL_API_KEY"])  # Replace with your default API key or leave it for dynamic setting.

token_set = nkeypass.TokenSet("0x79E812A3A530a42EA963B0E3Fd7f198Cc5C2C584", [4])
#@app.options("/chat", tags=["chat"])
#async def chat_endpoint(request: Request):
#    return JSONResponse(headers={"Allow": "OPTIONS,POST"}, content={})

@app.options("/chat")
async def handle_options():
    return {"Allow": "POST, OPTIONS", "Access-Control-Allow-Origin": "*"}

@app.post("/chat", tags=["chat"])
async def chat_endpoint(request: Request):
    print(f"request: {request.client}")
    await nkeypass.validate_access(request, token_set)
    # Retrieve the message and API token from the request
    user_message = await request.json()
    user_message = user_message["message"]
    #api_key = chat_request.api_token

    # Create a new Mistral client with the provided API token
    #mistral_client = Mistral(api_key=api_key)
    # Call the chat completion method
    chat_response = mistral_client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": user_message,
            },
        ]
    )

    # Return the response content
    return {"response": chat_response.choices[0].message.content}
