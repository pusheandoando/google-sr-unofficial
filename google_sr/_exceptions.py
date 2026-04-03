# google_sr/_exceptions.py





class AudioLoadError(Exception):
    pass

class RecognitionError(Exception):
    pass

class NoResultsError(RecognitionError):
    pass