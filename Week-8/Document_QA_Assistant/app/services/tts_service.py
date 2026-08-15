from pathlib import Path
from gtts import gTTS
from deep_translator import GoogleTranslator
import re


class TTSService:

    # =========================================================
    # SUPPORTED LANGUAGES
    # =========================================================

    LANGUAGE_MAP = {
        "english": "en",
        "hindi": "hi",
        "marathi": "mr",

        "en": "en",
        "hi": "hi",
        "mr": "mr"
    }

    LANGUAGE_NAMES = {
        "en": "English",
        "hi": "Hindi",
        "mr": "Marathi"
    }

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):

        self.audio_folder = Path("audio")

        self.audio_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    # =========================================================
    # LANGUAGE CODE
    # =========================================================

    def get_language_code(self, language: str):

        language = language.lower().strip()

        if language not in self.LANGUAGE_MAP:

            raise ValueError(
                "Supported languages: English, Hindi, Marathi"
            )

        return self.LANGUAGE_MAP[language]

    # =========================================================
    # LANGUAGE NAME
    # =========================================================

    def get_language_name(self, language: str):

        language_code = self.get_language_code(
            language
        )

        return self.LANGUAGE_NAMES[
            language_code
        ]

    # =========================================================
    # TRANSLATION
    # =========================================================

    def translate_text(
        self,
        text: str,
        target_language: str
    ):

        target_language = self.get_language_code(
            target_language
        )

        # English does not need translation
        if target_language == "en":

            return text

        if not text.strip():

            return ""

        try:

            translator = GoogleTranslator(
                source="auto",
                target=target_language
            )

            translated_text = translator.translate(
                text
            )

            if not translated_text:

                raise ValueError(
                    "Translation returned empty text."
                )

            return translated_text

        except Exception as e:

            raise RuntimeError(
                f"Translation failed: {str(e)}"
            )

    # =========================================================
    # CLEAN TEXT
    # =========================================================

    def clean_text(self, text: str):

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # =========================================================
    # SPLIT LONG TEXT
    # =========================================================

    def split_text(
        self,
        text: str,
        max_chars: int = 2500
    ):

        text = self.clean_text(
            text
        )

        if not text:

            return []

        sentences = re.split(
            r"(?<=[.!?।])\s+",
            text
        )

        chunks = []

        current = ""

        for sentence in sentences:

            if (
                len(current)
                + len(sentence)
                + 1
                <= max_chars
            ):

                current += (
                    " " + sentence
                )

            else:

                if current.strip():

                    chunks.append(
                        current.strip()
                    )

                current = sentence

        if current.strip():

            chunks.append(
                current.strip()
            )

        return chunks

    # =========================================================
    # GENERATE AUDIO
    # =========================================================

    def generate_audio(
        self,
        text: str,
        language: str,
        filename: str = "tts_output"
    ):

        # -----------------------------------------------------
        # Get language
        # -----------------------------------------------------

        language_code = (
            self.get_language_code(
                language
            )
        )

        # -----------------------------------------------------
        # Validate text
        # -----------------------------------------------------

        if not text or not text.strip():

            raise ValueError(
                "No text available."
            )

        # -----------------------------------------------------
        # Translate if required
        # -----------------------------------------------------

        translated_text = (
            self.translate_text(
                text=text,
                target_language=language_code
            )
        )

        # -----------------------------------------------------
        # Split translated text
        # -----------------------------------------------------

        chunks = self.split_text(
            translated_text
        )

        if not chunks:

            raise ValueError(
                "No text available after translation."
            )

        # -----------------------------------------------------
        # Generate audio
        # -----------------------------------------------------

        generated_files = []

        for index, chunk in enumerate(
            chunks,
            start=1
        ):

            output_filename = (
                f"{Path(filename).stem}_"
                f"{language_code}_"
                f"{index}.mp3"
            )

            output_path = (
                self.audio_folder
                / output_filename
            )

            tts = gTTS(
                text=chunk,
                lang=language_code,
                slow=False
            )

            tts.save(
                str(output_path)
            )

            generated_files.append(
                output_filename
            )

        # -----------------------------------------------------
        # Return result
        # -----------------------------------------------------

        return {
            "files": generated_files,
            "language": language_code,
            "language_name": self.LANGUAGE_NAMES[
                language_code
            ],
            "translated_text": translated_text
        }