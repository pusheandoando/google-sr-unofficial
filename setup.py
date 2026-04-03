# setup.py
from setuptools import setup, find_packages





with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name = "google-sr-unofficial",
    version = "1.0.0",
    description = "Unofficial Google Speech Recognition — no API key required.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = "Christian (@pusheandoando)",
    url = "https://github.com/pusheandoando/google-sr-unofficial",
    packages = find_packages(),
    python_requires = ">=3.9",
    install_requires = [
        "soundfile>=0.12.0",
        "numpy>=1.21.0",
        "pydub>=0.25.0",
    ],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
)