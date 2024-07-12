from src.phonemize.transcriber import transcribe_audio
from src.phonemize.analyzer import levenshtein_detailed, print_phonemes_with_indices, get_phonemes


def provide_detailed_feedback(user_phonemes, correct_phonemes):
    """ Generate detailed feedback for phoneme corrections. """
    operations = levenshtein_detailed(user_phonemes, correct_phonemes)
    user_phonemes_indices = print_phonemes_with_indices(user_phonemes)
    correct_phonemes_indices = print_phonemes_with_indices(correct_phonemes)
    feedback_lines = [
        "Fonemas transcritos: " + user_phonemes_indices,
        "Fonemas correctos: " + correct_phonemes_indices,
        "\nOperaciones necesarias:\n" + "\n".join(operations) if operations else "No se requieren cambios, la pronunciación es correcta."
    ]
    return "\n".join(feedback_lines)

# Ejemplo de uso
if __name__ == "__main__":
    audio_file = "output_file.wav"
    transcribed_text = transcribe_audio(audio_file)
    expected_text = "I want to be the champion of the American Cup again the last Di Maria's match"
    print(f'transcribed text: ', transcribed_text)
    print(f'expected text: ', expected_text)
    user_phonemes = get_phonemes(transcribed_text)
    correct_phonemes = get_phonemes(expected_text)

    feedback = provide_detailed_feedback(user_phonemes, correct_phonemes)
    print(feedback)
