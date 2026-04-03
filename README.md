# google-sr-unofficial
Unofficial Google Speech Recognition library for Python. No API key required.





## Install
```bash
pip3 install git+https://github.com/pusheandoando/google-sr-unofficial.git
```





## Usage
### With an audio file:
```python
from google_sr import recognize_audio_file

transcript = recognize_audio_file("audio.wav")
print(transcript)
```

With a different language:
```python
from google_sr import recognize_audio_file

transcript = recognize_audio_file("audio.flac", language="es-MX")
print(transcript)
```

Getting the raw API result:
```python
from google_sr import recognize_audio_file

result = recognize_audio_file("audio.wav", show_all=True)
print(result)
```

Listing supported languages:
```python
from google_sr import get_supported_languages

for code, name in get_supported_languages().items():
    print(f"{code}: {name}")
```





## Notes
- Audio is best recognized when it is clear, at least 8 kHz, and no longer than ~15 seconds per call (the API is designed for short utterances and commands).