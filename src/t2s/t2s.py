from gtts import gTTS
from io import BytesIO
from config.config import t2s_config

def text_to_speech(text, language=t2s_config['language']):
    # Ajustar el código de idioma si es necesario
    if language == 'en':
        language = 'en-us'
    elif language == 'fr':
        language = 'fr'
    elif language == 'it':
        language = 'it'
    elif language == 'pt':
        language = 'pt-br'
    elif language == 'es':
        language = 'es'

    # Crear un objeto gTTS
    tts = gTTS(text=text, lang=language)

    # Usar BytesIO para guardar el archivo de audio en memoria
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)  # Mover el cursor al inicio del stream

    return mp3_fp