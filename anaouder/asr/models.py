from typing import List

import os
import platform
import urllib
import zipfile
from tqdm import tqdm

from vosk import Model, SetLogLevel


DEFAULT_MODEL = "vosk-model-br-0.9"

_MODELS = {
    "vosk-model-br-0.6": "https://github.com/gweltou/vosk-br/releases/download/v0.6/vosk-model-br-0.6.zip",
    "vosk-model-br-0.7": "https://github.com/gweltou/vosk-br/releases/download/v0.7/vosk-model-br-0.7.zip",
    "vosk-model-br-0.8": "https://github.com/gweltou/vosk-br/releases/download/v0.8/vosk-model-br-0.8.zip",
    "vosk-model-br-0.9": "https://github.com/gweltou/vosk-br/releases/download/v0.9/vosk-model-br-0.9.zip",
}

_MODELS_ALIASES = {
    "vosk-br-0.6": "vosk-model-br-0.6",
    "vosk6": "vosk-model-br-0.6",
    "vosk-br-0.7": "vosk-model-br-0.7",
    "vosk7": "vosk-model-br-0.7",
    "vosk-br-0.8": "vosk-model-br-0.8",
    "vosk8": "vosk-model-br-0.8",
    "vosk-br-0.9": "vosk-model-br-0.9",
    "vosk9": "vosk-model-br-0.9",
    "vosk": "vosk-model-br-0.9",
}

_loaded_model = None
_loaded_model_name = ""


def available_models() -> List[str]:
    """ Returns the names of available models
        Code modified from https://github.com/openai/whisper
    """
    return list(_MODELS.keys())


def load_model(
    model_name: str = None,
    download_root: str = None,
) -> Model:
    """Code modified from https://github.com/openai/whisper"""
    global _loaded_model_name
    global _loaded_model
    
    if model_name == None:
        if _loaded_model:
            return _loaded_model
        model_name = DEFAULT_MODEL
    
    if model_name == _loaded_model_name:
        return _loaded_model

    if model_name in _MODELS_ALIASES:
        model_name = _MODELS_ALIASES[model_name]

    if download_root is None:
        if platform.system() in ("Linux", "Darwin"):
            default = os.path.join(os.path.expanduser("~"), ".cache")
        elif platform.system() == "Windows":
            default = os.getenv("LOCALAPPDATA")
        else:
            raise OSError('Unsupported operating system')
        download_root = os.path.join(os.getenv("XDG_CACHE_HOME", default), "anaouder", "models")

    if model_name in _MODELS:
        model_path = _download(model_name, download_root)
    elif os.path.isdir(model_name):
        model_path = model_name
    else:
        raise RuntimeError(
            f"Model {model_name} not found; available models = {available_models()}"
        )

    print("Loading", os.path.basename(model_path))
    SetLogLevel(-1)
    _loaded_model = Model(model_path)
    _loaded_model_name = model_name

    return _loaded_model


def _download(model_name: str, root: str) -> str:
    """ Code modified from https://github.com/openai/whisper
        Get the requested model path on disk or download it if not present
    """
    os.makedirs(root, exist_ok=True)
    url = _MODELS[model_name]
    
    download_target = os.path.join(root, os.path.basename(url))
    model_path = os.path.join(root, model_name)

    if os.path.isdir(model_path):
        return model_path

    print("Downloading model from", url)

    with urllib.request.urlopen(url) as source, open(download_target, "wb") as output:
        with tqdm(
            total=int(source.info().get("Content-Length")),
            ncols=80,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as loop:
            while True:
                buffer = source.read(8192)
                if not buffer:
                    break

                output.write(buffer)
                loop.update(len(buffer))
    
    with zipfile.ZipFile(download_target, 'r') as zip_ref:
        zip_ref.extractall(root)

    os.remove(download_target)

    return model_path
