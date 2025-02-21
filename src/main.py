from fastapi import FastAPI, HTTPException,Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from pathlib import Path
from typing import Dict
import re
import logging



app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://staging.telextest.im", "http://telextest.im", "https://staging.telex.im", "https://telex.im"], # NB: telextest is a local url
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Message(BaseModel):
    text: str

# Load acronyms from JSON file
def load_acronyms() -> Dict[str, str]:
    try:
        # Use absolute path for reliability
        current_dir = Path(__file__).parent
        json_path = current_dir / "acronym.json"
        
        with open(json_path, "r") as f:
            acronyms = json.load(f)
        
        # Normalize acronyms to lowercase for case-insensitive matching
        return {k.lower(): v for k, v in acronyms.items()}
    
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="acronym.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in acronym.json")

# Access integration.json in the root directory
def load_integration ():
    # Access integration.json in the root directory
    try:
        root_dir = Path(__file__).parent.parent
        integration_path = root_dir / "integration.json"
        with open(integration_path, "r") as f:
                return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="integration.json not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in integration.json")


# A function to to handle the acronym expander logic
def Acronym_expand(text:str, acronym:Dict[str, str]):
    # sorting the acronyms in descending order
    sorted_acronyms = sorted(acronym.items(), key=lambda x: len(x[0]), reverse= True)
    # Replace acronyms case-insensitively using regex
    for acronym, full_form in sorted_acronyms:
            pattern = re.compile(re.escape(acronym), re.IGNORECASE)
            text= pattern.sub(full_form, text)
    return text

@app.get("/integration.json")
def get_integration_json(request: Request):
    integration = load_integration()
    return integration

@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.json()
        logger.info("body: %s", body)
        message = body.get("message")
        if not message:
            raise HTTPException(status_code=422, detail="Message text is required")
        logger.info("mesage: %s", message)
        settings = body.get("settings")
        logger.info("settings: %s", settings)
        return {"message": f'message{message}'}
    except Exception as e:
        logger.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/expand")
async def expand_acronyms(request: Request):
    try:
        body = await request.json()
        logger.info("body: %s", body)
        message = body.get("message")
        if not message:
            raise HTTPException(status_code=422, detail="Message text is required")
        logger.info("mesage: %s", message)
        acronyms = load_acronyms()
        
        messages = Acronym_expand(message, acronyms)


        return {"status": "success", "message": messages}
    except Exception as e:
        logger.error("Error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    logger.info("FastAPI is listening at http://localhost:8000")
  