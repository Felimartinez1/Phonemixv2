from fastapi import FastAPI, UploadFile, File, Response
from src.phonemize.analyzer import get_phonemes
from src.phonemize.transcriber import transcribe_audio
from src.phonemix import provide_detailed_feedback
from src.t2s.t2s import text_to_speech
import uvicorn
import base64
from io import BytesIO

app = FastAPI()

@app.post("/feedback/")
async def pronunciation_feedback(file: UploadFile = File(...), expected_text: str = "", language: str = "es"):
    # Save the uploaded file
    
    # Leer el contenido del archivo cargado y convertirlo en un stream en memoria
    file_content = await file.read()
    user_audio_stream = BytesIO(file_content)
    
    # Guardar temporalmente el archivo para procesamiento
    audio_file = f"/tmp/{file.filename}"
    with open(audio_file, "wb") as f:
        f.write(file_content)
        
    # Convertir el audio del usuario a base64
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
    uvicorn.run(app, host="localhost", port=8000)