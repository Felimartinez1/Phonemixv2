from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from src.phonemize.analyzer import get_phonemes
from src.phonemize.transcriber import transcribe_audio
from src.phonemix import provide_detailed_feedback
from src.t2s.t2s import text_to_speech
import uvicorn
import base64
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Welcome to the Pronunciation Feedback API"}

@app.post("/feedback/")
async def pronunciation_feedback(file: UploadFile = File(...), expected_text: str = "", language: str = ""):
    print(file, expected_text, language) 
    # Read the content of the loaded file and convert it to an in-memory stream
    file_content = await file.read()
    user_audio_stream = BytesIO(file_content)
    
    # Temporarily save the file for processing
    audio_file = f"/tmp/{file.filename}"
    with open(audio_file, "wb") as f:
        f.write(file_content)
        
    # Convertir user audio to base64
    user_audio_base64 = base64.b64encode(user_audio_stream.getvalue()).decode('utf-8')

    # Transcribe the audio file and get phonemes
    transcribed_text = transcribe_audio(audio_file, language)
    user_phonemes = get_phonemes(transcribed_text, language)

    # Generate expected audio and convert it to base64
    expected_audio_stream = text_to_speech(expected_text, language)
    expected_audio_base64 = base64.b64encode(expected_audio_stream.read()).decode('utf-8')

    correct_phonemes = get_phonemes(expected_text, language)

    # Generate feedback
    feedback = provide_detailed_feedback(user_phonemes, correct_phonemes)

    return {
        "user_audio": "data:audio/mpeg;base64," + user_audio_base64,
        "user_text": transcribed_text,
        "user_phonemes": user_phonemes,
        "expected_audio": "data:audio/mpeg;base64," + expected_audio_base64,
        "expected_text": expected_text,
        "expected_phonemes": correct_phonemes,
        "feedback": feedback
    }

if __name__ == "__main__":
    uvicorn.run(app, host="ec2-13-56-160-76.us-west-1.compute.amazonaws.com", port=8000)
