# Anaouder mouezh e brezhoneg

M'ho peus c'hoant sikour ar raktres gant un donezon :

[![Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/gweltou/donate)


## Petra eo ?

Amañ e vez kinniget ur model anaouder mouezh da implijout gant ar meziant [Vosk](https://github.com/alphacep/vosk-api).\
Gantañ e c'heller adskrivañ komzoù e brezhoneg (**Son -> Skrid**) en un doare emgefre, dre ur mikro e amzer real pe diouzh restroù son.\
Pleustret eo bet gant un dek a eurvezh bennak (roadennoù son ha skrid linennet), dre ar "framework" [Kaldi](https://www.kaldi-asr.org/).

Ar modeloù pleustret gant Kaldi n'int ket ar re efedusañ, e-keñver modeloù nevesoc'h, met perzhioù dedennus o deus memes tra :

 * **Skañv**. Ar model e brezhoneg ne ra nemet 60 Mo ha treiñ a ra war ur bern mekanikoù : urzhiataerioù **hep GPU**, RaspberryPi, hezoug Android...
 * **Prim**. Gallout a reer adskrivañ ar son e **amzer real**, memes gant un urzhiataer kozh, pe primoc'h c'hoazh gant dafar dereat.
 * **Lec'hel**. Ezhomm ebet eus an Internet. Ho mouezh hag **ho restroù son a chomo war ho penveg** ha tretet e vint gant ho penveg nemetken. Kudenn surentez ebet liammet d'an treuzkas dre rouedad ha gwelloc'h a-fed ekologel.
 * **Digoust ha dieub**. Gellout a reoc'h azasaat ar meziant d'hoc'h ezhommoù pe enframmañ anezhañ e meziantoù all.

Dalc'hoù zo siwazh :
 * Poentadur ebet.
 * Kizidig d'an trouzioù endro.
 * Fall war ur bern pouezioù-mouez c'hoazh.
 * Ret eo komz sklaer ha goustadig.

Emichañs e vo gwellaet efedusted an anaouder tamm-ha-tamm, gant ma vo kavet roadennoù mouezh adskrivet.\
Ul lisañs dieub (doare [Creative Commons](https://creativecommons.org/licenses/)) a aotre da eskemm ar roadennoù en un doare aes.


## Staliañ

An doare da staliañ a cheñch hervez ho sistem oberiant (Linux, Windows pe MacOS). Deoc'h da furchal evit gouzout penaos ober evit ho hini.


### ffmpeg

Ezhomm ho po ar meziant `ffmpeg` evit ma c'hellfe an anaouder digeriñ ar restroù son pe video e stumm-mañ-stumm.

https://ffmpeg.org/download.html

Ur wech staliet e ranker bezañ gouest da zigeriñ un terminal ha peurgas an urzh-mañ hep fazi :

```bash
ffmpeg -version
```

### Python3

Ezhomm ho po staliañ ar yezh programiñ `python3` (alies eo staliet dre ziwer war ar sistemoù Linux, met ket war Windows pe MacOS)

https://www.python.org/downloads/

Da c'houde ho po da staliañ ar moduloù da-heul, dre ar meziant `pip3` (staliet gant python3).

```bash
pip install sounddevice
pip install vosk
```

Muioc'h a ditouroù a c'heller kavout evit staliañ `vosk` war al [lec'hienn ofisiel](https://alphacephei.com/vosk/install#python-installation-from-pypi).


### Anaouder

Ur wech bezañ bet staliet `ffmpeg` ha `python3` e c'heller pellkargañ an anaouder, o klikañ war ar bouton "code" gwer ha dibab "Download ZIP". Diwaskit an teuliad en un lec'h bennak war ho urzhiataer.


## Adskrivañ ur restr son

Gant ar skript `adskrivan_ffmpeg.py` e vo adskrivet ar pezh e vez komprenet gant an anaouder diouzh ur restr son.

``python3 adskrivan_ffmpeg.py ANV_RESTR.mp4``


## Linennañ ur teul skrid gant un teul son

M'ho peus un teul skrid adskrivet dre dorn (e stumm `.txt`) e c'heller linennañ ar skrid gant ar son, evit krouiñ ur restr istitloù (e stumm `srt`).

``python3 linennan.py SON.mp3 SKRID.txt``

Gant an option `-o` ez eus tu reiñ anv ur restr e lerc'h ma vo skrivet an istitloù, da skouer :

``python3 linennan.py SON.mp3 SKRID.txt -o istitloù.srt``


## Implijout gant ur mikro

Evit gouzout niverenn an etrefas son :

``python3 mikro.py -l``

Ha gant an niverenn-se :

``python3 mikro.py -d NIVERENN_ETREFAS``


## Adskrivañ istitloù evit ur video

Gant vosk e c'heller adskrivañ teuliadoù son ha filmoù evit kaout ur restr e stumm `srt`.

Da skouer:

``python3 istitlan.py Nozhvez_Digousk.mp4``

An oberiadur-se a gemero kalzig a amzer (hervez padelezh an teuliad son). Klaskit gant ur film berr da gentañ !

https://user-images.githubusercontent.com/10166907/213805292-63becbe2-ffb5-492f-9bac-1330c4b2d07d.mp4

*Setu disoc'h an iztitloù emgefre, hep cheñch netra. Gwelet vez e vez kollet buan pa vez sonnerez...*


## Implij gant meziantoù all

### Istitloù emgefre gant Kdenlive

(N'eo ket aliet dre ma vez kollet un nebeut perzhioù e-keñver ar pezh vez graet gant ar skript `isitlan.py`)

Gant ar meziant frammañ videoioù [Kdenlive](https://kdenlive.org/) e c'heller adskrivañ istitloù en un doare emgefre ivez.\
Ar mod-implij a c'heller kavout [amañ](https://docs.kdenlive.org/en/effects_and_compositions/speech_to_text.html).\
Kentoc'h eget pell-kargañ ur model war lec'hienn ofisiel vosk, implijit ar model diwezhañ a vo kavet gant al liamm "[releases](https://github.com/gweltou/Vosk-bzg/releases)".
