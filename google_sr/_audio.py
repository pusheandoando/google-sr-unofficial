# google_sr/_audio.py
import io
import os

import numpy as np
import soundfile as sf
from pydub import AudioSegment

from google_sr._exceptions import AudioLoadError





_SOUNDFILE_FORMATS = {
    ".wav", ".flac", ".aiff", ".aif",
    ".au", ".rf64", ".ogg", ".opus"
}
_PYDUB_FORMATS = {
    ".mp3", ".m4a",".wma", ".aac"
}





def _from_soundfile(filepath):
    try:
        data, samplerate = sf.read(filepath, dtype="float32", always_2d=True)
    except Exception as exc:
        raise AudioLoadError(f"[google_sr] failed to read '{filepath}': {exc}") from exc

    data = data.mean(axis=1)
    data = (data * 32767).clip(-32768, 32767).astype(np.int16)
    return data, samplerate


def _from_pydub(filepath):
    try:
        seg = AudioSegment.from_file(filepath).set_channels(1)
    except Exception as exc:
        raise AudioLoadError(f"[google_sr] failed to read '{filepath}': {exc}") from exc

    samplerate = seg.frame_rate
    samples = np.array(seg.get_array_of_samples(), dtype=np.int16)
    return samples, samplerate


def load_as_flac(filepath):
    ext = os.path.splitext(filepath)[-1].lower()

    if ext in _SOUNDFILE_FORMATS:
        data, samplerate = _from_soundfile(filepath)
    elif ext in _PYDUB_FORMATS:
        data, samplerate = _from_pydub(filepath)
    else:
        try:
            data, samplerate = _from_soundfile(filepath)
        except AudioLoadError:
            data, samplerate = _from_pydub(filepath)

    if samplerate < 8000:
        raise AudioLoadError(f"[google_sr] sample rate {samplerate}hz is below the 8000hz minimum required by Google Speech API, resample the audio to at least 8000hz first.")

    buf = io.BytesIO()
    sf.write(buf, data, samplerate, format="FLAC", subtype="PCM_16")
    buf.seek(0)
    return buf.read(), samplerate