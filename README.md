# Vosk e Brezhoneg

Anaouder vouezh e brezhoneg dre ar meziant [Vosk](https://github.com/alphacep/vosk-api).

## Petra eo ?

Amañ e vez kinniget ur model anaouder vouezh da implij gant ar meziant [Vosk](https://github.com/alphacep/vosk-api).

Gantañ e c'heller adskrivañ komzoù e brezhoneg (**Son -> Skrid**) en un doare emgefre, dre ur mikro e amzer real pe diouzh restroù son.

Pleustret eo bet gant un dek a eurvezh bennak nemetken (roadennoù son ha skrid linennet) dre ar "framework" [Kaldi](https://www.kaldi-asr.org/).

Ar modeloù pleustret gant Kaldi n'int ket ar re efedusañ, e-keñver ar modeloù a vez kinniget gant embregerezhioù bras, evel Facebook (Wav2Vec 2.0) pe OpenAI (Whisper) met perzhioù dedennus o deus memes tra :

 * **Skañv**. Ar model e brezhoneg ne ra nemet 60 Mo ha treiñ a ra war ur bern mekanikoù : urzhiataerioù **hep GPU**, RaspberryPi, hezoug Android...
 * **Prim**. Gallout a reer adskrivañ ar son e **amzer real**, memes gant un urzhiataer kozh, pe primoc'h c'hoazh gant dafar dereat.
 * **Lec'hel**. Ezhomm ebet eus an Internet. Ho mouezh hag **ho restroù son a chomo war ho benveg** ha tretet e vint gant ho benveg nemetken. Kudenn surentez ebet liammet d'an treuzkas dre rouedad ha gwelloc'h a-fed ekologel !
 * **Digoust ha dieub**. Gellout a reoc'h azasaat ar meziant d'ho ezhommoù pe enframmañ anezhañ e meziantoù all.

Dalc'hoù zo siwazh : re diefedus eo c'hoazh evit bezañ pleustrek. Emichañs e vo gwellaet efedusted an anaouder tamm-ha-tamm, gant ma vo kavet roadennoù mouezh adskrivet hag gant gwirioù dieub (doare [Creative Commons](https://creativecommons.org/licenses/))

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

https://user-images.githubusercontent.com/10166907/213805292-63becbe2-ffb5-492f-9bac-1330c4b2d07d.mp4

*Setu disoc'h an iztitloù emgefre, hep cheñch netra. Gwelet vez e vez kollet buan pa vez sonnerez...*

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
