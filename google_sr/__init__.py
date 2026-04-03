# google_sr/__init__.py
from google_sr.recognizers.audio_file import recognize_audio_file
from google_sr._languages import SUPPORTED_LANGUAGES, get_supported_languages
from google_sr._exceptions import AudioLoadError, NoResultsError, RecognitionError





__version__ = "1.0.0"
__all__ = [
    "recognize_audio_file",
    "get_supported_languages",
    "SUPPORTED_LANGUAGES",
    "AudioLoadError",
    "RecognitionError",
    "NoResultsError",
]