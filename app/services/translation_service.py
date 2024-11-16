from googletrans import Translator

translator = Translator()

def translate_message(text: str, dest_language: str) -> str:
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text  # En caso de error, retorna el texto original
