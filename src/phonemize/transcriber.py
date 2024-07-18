import subprocess
import os
import speech_recognition as sr
from config.config import phonemize_config


def convert_audio(input_file, output_file):
    """ Convert audio file to desired format using ffmpeg. """
    command = ['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', output_file, '-y']
    subprocess.run(command, check=True)

def transcribe_audio(audio_file, phoneme_language=phonemize_config['language']):
    """ Transcribe audio to text using Google's speech recognition service, adjusting the language based on phoneme settings. """
    temp_file = '/tmp/temp_converted_audio.wav'
    try:
        # Convert the audio file
        convert_audio(audio_file, temp_file)

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_file) as source:
            audio_data = recognizer.record(source)
            try:
                if phoneme_language == 'es':
                    return recognizer.recognize_google(audio_data, language='es-ES')
                elif phoneme_language == 'en':
                    return recognizer.recognize_google(audio_data, language='en')
                elif phoneme_language == 'it':
                    return recognizer.recognize_google(audio_data, language='it')
                elif phoneme_language == 'fr':
                    return recognizer.recognize_google(audio_data, language='fr') 
                elif phoneme_language == 'pt':
                    return recognizer.recognize_google(audio_data, language='pt-br')
            except sr.UnknownValueError:
                return phonemize_config['unknownvaluerror']
            except sr.RequestError:
                return phonemize_config['requesterror']
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
