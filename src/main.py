from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import AsyncGroq
from pydantic import BaseModel
import json
import os
import csv

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def read_signal_strength(filename):
    # Lists to store the data
    frequencies = []
    strengths = []
    
    # Read the CSV file
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                freq = int(float(row['Frequency']))  # Convert to int for cleaner numbers
                strength = float(row['Signal_Strength'])
                frequencies.append(freq)
                strengths.append(strength)
                
    except FileNotFoundError:
        print(f"Could not find file: {filename}")
        return
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        return
    
    # return the signal strength
    return  strengths, frequencies


# Initialize the FastAPI app once
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the Groq client (assuming API key is set in environment)
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))  # Set your API key in env or here directly
router = APIRouter()

# Define the data schema
class FrequencyReport(BaseModel):
    provider: str
    strength: float
    technology: str
    service: str
    frequency_range: str
    
class FrequencyInput(BaseModel):
    user_message: str

@router.post("/prompt")
async def generate_report(request: FrequencyInput):  # Made async
    """
    Check compliance for the user message.
    """
    try:
        
        # Write code here 
        print("Antler Hackathon Frequency Analyzer")
        sstr, freq = read_signal_strength('max_signal_strengths.csv')

        
        chat_completion = await client.chat.completions.create(  # Added await
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in frequency analysis." 
                        f"The variable {sstr} refers to the signal strength and the variable {freq} refers to the corresponding frequencies from a frequency scan"
                        "With publically available knowledge, can you summarize what kinds of services, providers,technology are being used?"
                        f" Output should be in the JSON format as an array using the schema: {json.dumps(FrequencyReport.model_json_schema(), indent=2)}"
                    ),
                },
                {
                    "role": "user",
                    "content": request.user_message,
                },
            ],
            model="llama-3.3-70b-versatile",
            temperature=0,
            top_p=1,
            response_format={"type": "json_object"},
        )

        
        # Return the content from the completion
        return json.loads(chat_completion.choices[0].message.content)  # Parse JSON string to dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Include the router in the app
app.include_router(router)

# Optional: Add a root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Server is running"}