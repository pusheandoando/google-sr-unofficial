# google_sr/recognizers/audio_file.py
from google_sr._audio import load_as_flac
from google_sr._api import _DEFAULT_KEY, recognize





def recognize_audio_file(filepath, language="en-US", pfilter=0, show_all=False, key=None, timeout=30, retries=3):
    flac_data, sample_rate = load_as_flac(filepath)
    
    return recognize(
        flac_data = flac_data,
        sample_rate = sample_rate,
        language = language,
        pfilter = pfilter,
        show_all = show_all,
        key = key or _DEFAULT_KEY,
        timeout = timeout,
        retries = retries,
    )