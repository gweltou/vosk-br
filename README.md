# Vosk e Brezhoneg

Anaouder yezh e brezhoneg dre ar meziant [Vosk](https://github.com/alphacep/vosk-api).

Gwellaet e vezo efedusted an anaouder tamm-ha-tamm, gant ma vo kavet roadennoù mouezh adskrivet hag gant gwirioù dieub (doare [Creative Commons](https://creativecommons.org/licenses/))

## Staliañ

```bash
pip3 install sounddevice
pip3 install vosk
```

Muioc'h a titouroù a c'hellit kavout war [lec'hienn ofisiel Vosk](https://alphacephei.com/vosk/install#python-installation-from-pypi).

## Adskrivañ ur restr son

Ret eo amdreiñ ar restr son e stumm PCM mono 16bit, 16KHz sampling rate.

Gant ar meziant `ffmpeg` e c'heller ober en un doare prim :

``ffmpeg -i ANV_RESTR.mp3 -acodec pcm_s16le -ac 1 -ar 16000 ANV_RESTR.wav``

Ha da c'houde :

``python3 test_wavefile.py ANV_RESTR.wav``
 
## Implij gant ur mikro

Evit gouzout niverenn an etrefas son :

``python3 test_microphone.py -l``

Ha gant an niverenn-se :

``python3 test_microphone.py -d NIVERENN_ETREFAS``

## Adskrivañ iztitloù evit ur video

### Dre an terminal

Gant vosk e c'hellit adskrivañ teuliadoù son ha filmoù evit kaout ur restr e stumm `srt`.

Ezhomm ho po e vefe staliet ar meziant `ffmpeg` evit implij ar perzh-se (evit amdreiñ a restroù e stumm PCM 16bit, 16KHz).

Da skouer:

``python3 test_srt.py Nozhvez_Digousk.mp4``

An oberiadur-se a gemero kalzig a amzer (hervez padelezh an teuliad son). Klaskit gant ur film berr da gentañ !

### E diabarzh Kdenlive

Gant ar meziant frammañ videoioù [Kdenlive](https://kdenlive.org/) e c'heller adskrivañ iztitloù en un doare emgefre ivez.

Ar mod-implij a c'heller kavout [amañ](https://docs.kdenlive.org/en/effects_and_compositions/speech_to_text.html).

Kentoc'h eget pellkargañ ur model war lec'hienn ofisiel vosk, implijit ar model diwezhañ a vo kavet gant al liamm "[releases](https://github.com/gweltou/Vosk-bzg/releases)".