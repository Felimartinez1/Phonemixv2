from fastapi import FastAPI, UploadFile, File
from src.phonemize.analyzer import get_phonemes
from src.phonemize.transcriber import transcribe_audio
from src.phonemix import provide_detailed_feedback
import uvicorn

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to Phonemix, the Pronunciation Feedback API. Use the /feedback endpoint to get detailed feedback on your pronunciation."}

@app.post("/feedback/")
async def pronunciation_feedback(file: UploadFile = File(...), expected_text: str = "", language: str = "es"):
    # Save the uploaded file
    audio_file = f"/tmp/{file.filename}"
    with open(audio_file, "wb") as f:
        f.write(await file.read())
    
    # Transcribe the audio file and get phonemes
    transcribed_text = transcribe_audio(audio_file, language)
    user_phonemes = get_phonemes(transcribed_text, language)
    
    # Translate the expected text to the expected language
    # expected_text = t2tt(expected_text)
    correct_phonemes = get_phonemes(expected_text, language)
    
    # Generate feedback
    feedback = provide_detailed_feedback(user_phonemes, correct_phonemes)
    
    return {
        "user_audio": audio_file,
        "user_text": transcribed_text,
        "user_phonemes": user_phonemes,
        "expected_text": expected_text,
        "expected_phonemes": correct_phonemes,
        "feedback": feedback
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    
# uvicorn app:app --reload