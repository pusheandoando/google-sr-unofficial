# google_sr/_api.py
import json
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from google_sr._exceptions import NoResultsError, RecognitionError





# my api key? chill babe, it's from: https://gist.github.com/alotaiba/1730160
_DEFAULT_KEY = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
ENDPOINT = "https://www.google.com/speech-api/v2/recognize"





def _build_url(language, key, pfilter):
    params = urlencode({
        "client": "chromium",
        "lang": language,
        "key": key,
        "pFilter": pfilter,
    })
    return f"{ENDPOINT}?{params}"


def _send(flac_data, sample_rate, language, key, pfilter, timeout):
    url = _build_url(language, key, pfilter)
    headers = {"Content-Type": f"audio/x-flac; rate={sample_rate}"}
    req = Request(url, data=flac_data, headers=headers)
    
    try:
        response = urlopen(req, timeout=timeout)
    except HTTPError as exc:
        raise RecognitionError(f"[google_sr] Google Speech API returned HTTP {exc.code}: {exc.reason}") from exc
    except URLError as exc:
        raise RecognitionError(f"[google_sr] could not reach Google Speech API: {exc.reason}") from exc
    return response.read().decode("utf-8")


def _parse(response_text, show_all):
    for line in response_text.splitlines():
        if not line:
            continue
        
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        results = data.get("result", [])
        if not results:
            continue

        result = results[0]
        if show_all:
            return result

        alternatives = result.get("alternative", [])
        if not alternatives:
            raise NoResultsError("[google_sr] Google Speech API returned results but no alternatives.")

        if len(alternatives) > 1 and "confidence" in alternatives[0]:
            best = max(alternatives, key=lambda a: a.get("confidence", 0.0))
        else:
            best = alternatives[0]

        transcript = best.get("transcript", "")
        if not transcript:
            raise NoResultsError("[google_sr] Google Speech API returned an empty transcript.")

        return transcript
    raise NoResultsError("[google_sr] Google Speech API returned no transcription, the audio may be silent, too short, or in an unsupported language.")


def recognize(flac_data, sample_rate, language, pfilter, show_all, key, timeout, retries):
    last_exc = None
    
    for attempt in range(max(1, retries)):
        try:
            raw = _send(flac_data, sample_rate, language, key, pfilter, timeout)
            return _parse(raw, show_all)
        except NoResultsError:
            raise
        except RecognitionError as exc:
            last_exc = exc
            
            if attempt < retries - 1:
                time.sleep(1.5 ** attempt)
    raise last_exc