from os import path
from setuptools import setup, find_packages


NAME = "anaouder"
DESCRIPTION = "Breton language speech-to-text tools"
URL = "https://github.com/gweltou/vosk-br"
AUTHOR = "Gweltaz Duval-Guennoc"
EMAIL = "gweltou@hotmail.com"
VERSION = "0.7.9"
REQUIRES_PYTHON = ">=3.6.0"


# The directory containing this file
HERE = path.dirname(__file__)

with open(path.join(HERE, "requirements.txt")) as fd:
    REQUIREMENTS = [line.strip() for line in fd.readlines() if line.strip()]


setup(
    name=NAME,
    url=URL,
    version=VERSION,
    author=AUTHOR,
    licence="MIT",
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIREMENTS,
    classifiers=[
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Operating System :: OS Independent"
	],
    packages=find_packages(),
    # package_dir={"anaouder": "anaouder", "ostilhou": "anaouder/ostilhou"},
    package_data={
        "anaouder": [
            "models/vosk-model-br-0.7/*",
            "models/vosk-model-br-0.7/ivector/*",
            "ostilhou/asr/inorm_units.tsv",
            "ostilhou/asr/postproc_sub.tsv",
            "ostilhou/dicts/acronyms.tsv",
            "ostilhou/dicts/corrected_tokens.tsv",
            "ostilhou/dicts/named_entities.tsv",
            "ostilhou/dicts/noun_f.tsv",
            "ostilhou/dicts/noun_m.tsv",
            "ostilhou/dicts/proper_nouns_phon.tsv",
        ]
    },
    data_files=[('', ["README-fr.md", "CHANGELOG.txt"])],
    entry_points={
        "console_scripts": [
            "adskrivan = anaouder:main_adskrivan",
            "linennan = anaouder:main_linennan",
            "istitlan = anaouder:main_istitlan",
            "mikro = anaouder:main_mikro",
        ],
    },
)
