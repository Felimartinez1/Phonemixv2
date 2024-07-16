from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.phonemize.analyzer import get_phonemes
from src.phonemize.transcriber import transcribe_audio
from src.phonemix import provide_detailed_feedback
from src.t2s.t2s import text_to_speech
import uvicorn
import base64
from io import BytesIO
from pydub import AudioSegment
import os

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
async def pronunciation_feedback(file: UploadFile = File(...), expected_text: str = Form(...), language: str = Form("es")):
    if not expected_text:
        raise HTTPException(status_code=400, detail="Expected text is required.")
    
    try:
        # Read the content of the loaded file and convert it to an in-memory stream
        file_content = await file.read()
        user_audio_stream = BytesIO(file_content)
        
        # Convert the audio to PCM WAV format using pydub
        audio_segment = AudioSegment.from_file(user_audio_stream)
        audio_file = f"/tmp/{file.filename}.wav"
        audio_segment.export(audio_file, format="wav")

        # Convertir user audio to base64
        user_audio_base64 = base64.b64encode(file_content).decode('utf-8')

        # Transcribe the audio file and get phonemes
        transcribed_text = transcribe_audio(audio_file, language)
        user_phonemes = get_phonemes(transcribed_text, language)

        # Generate expected audio and convert it to base64
        expected_audio_stream = text_to_speech(expected_text, language)
        expected_audio_base64 = base64.b64encode(expected_audio_stream.read()).decode('utf-8')

        correct_phonemes = get_phonemes(expected_text, language)

        # Generate feedback
        feedback = provide_detailed_feedback(user_phonemes, correct_phonemes)

        # Clean up the temporary file
        os.remove(audio_file)

        return {
            "user_audio": "data:audio/mpeg;base64," + user_audio_base64,
            "user_text": transcribed_text,
            "user_phonemes": user_phonemes,
            "expected_audio": "data:audio/mpeg;base64," + expected_audio_base64,
            "expected_text": expected_text,
            "expected_phonemes": correct_phonemes,
            "feedback": feedback
        }

    except Exception as e:
        print(f"Error: {e}")  # Agregar más logs si es necesario
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="ec2-54-183-218-147.us-west-1.compute.amazonaws.com", port=8000)
