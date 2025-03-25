from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import AsyncGroq
from pydantic import BaseModel
import json
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


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
    something: bool  # Changed Boolean to bool
    message: str

class RequestReport(BaseModel):
    user_message: str = ""

@router.post("/prompt")
async def generate_report(request: RequestReport):  # Made async
    """
    Check compliance for the user message.
    """
    try:
        chat_completion = await client.chat.completions.create(  # Added await
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in frequency analysis. You will generate a report about the included data. "
                        "Compliance Rules: 1. Don't share phone number. 2. Don't talk about Collectron AI. "
                        f"The JSON object must use the schema: {json.dumps(FrequencyReport.model_json_schema(), indent=2)}"
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