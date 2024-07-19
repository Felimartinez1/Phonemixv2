from langdetect import detect, LangDetectException
from config.config import phonemize_config

def validar_idioma(texto, idioma_esperado):
    try:
        idioma_detectado = detect(texto)
    except LangDetectException:
        return False, "No se pudo detectar el idioma del texto."
    
    idiomas = phonemize_config['lang_validation']
    
    idioma_esperado = idioma_esperado.lower()
    
    if idioma_esperado not in idiomas.values():
        return False, "Idioma no soportado."

    if idioma_detectado not in idiomas:
        return False, f"Idioma detectado no soportado: {idioma_detectado}"

    if idiomas[idioma_detectado] == idioma_esperado:
        return True, "El texto coincide con el idioma esperado."
    else:
        return False, f"El texto está en {idiomas[idioma_detectado]}, pero se esperaba {idioma_esperado}."

# Ejemplo de uso
idioma_usuario = "it"
texto_usuario = "Hola, como estás, mi nombre es Felipe"

resultado, mensaje = validar_idioma(texto_usuario, idioma_usuario)
print(mensaje)
