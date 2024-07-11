import speech_recognition as sr


def transcribe_audio(audio_file, phoneme_language='en-us'):
    """ Transcribe audio to text using Google's speech recognition service, adjusting the language based on phoneme settings. """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            if phoneme_language == 'es':
                return recognizer.recognize_google(audio_data, language='es-ES')
            else:
                return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"