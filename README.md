[![pypi version](https://img.shields.io/pypi/v/anaouder)](https://pypi.org/project/anaouder/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

# Anaouder mouezh e brezhoneg gant Vosk

[Version française](https://github.com/gweltou/vosk-br/blob/main/README-fr.md)

## Petra eo ?

Un anaouder mouezh emgefre, graet gant ar meziantoù [Kaldi](https://www.kaldi-asr.org/) ha [Vosk](https://github.com/alphacep/vosk-api).\
Gantañ e c'heller adskrivañ komzoù e brezhoneg (**Son -> Skrid**) en un doare emgefre, dre ur mikro e amzer real pe diouzh restroù son.\
Pleustret eo bet gant un dek eurvezh bennak a deulioù son ha skrid linennet.

Un nebeut perzhioù dedennus :

* **Skañv**. Pouezh ar model a zo dindan 100 Mo ha treiñ a ra war ur bern mekanikoù : urzhiataerioù **hep GPU**, RaspberryPi, hezoug Android...
* **Prim**. Gallout a reer adskrivañ ar son e **amzer real**, memes gant un urzhiataer kozh, pe primoc'h c'hoazh gant dafar nevesoc'h.
* **Lec'hel**. Ezhomm ebet eus an Internet. Ho mouezh hag **ho data a chomo war ho penveg**, ha tretet e vint gant ho penveg nemetken. Kudenn surentez ebet liammet d'an treuzkas dre rouedad ha gwelloc'h a-fed ekologel.
* **Digoust ha dieub**. Gellout a reoc'h azasaat ar meziant d'hoc'h ezhommoù pe enframmañ anezhañ e meziantoù all.

Dalc'hoù 'zo siwazh :

* Poentadur ebet.
* Kizidig d'an trouzioù endro.
* Fall war ur bern pouezioù-mouezh c'hoazh.
* Ret eo komz sklaer ha goustadik.

Emichañs e vo gwellaet efedusted an anaouder tamm-ha-tamm, gant ma vo kavet roadennoù mouezh adskrivet.\
Ul lisañs dieub (doare [Creative Commons](https://creativecommons.org/licenses/)) a aotrefe eskemm ar roadennoù-se en un doare aes.

Sikour ar raktres gant un donezon :
[![Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/gweltou/donate)

## Staliañ

Goude bezañ bet staliet [Python3](https://www.python.org/downloads/) e c'heller staliañ an anaouder dre an terminal :

```bash
pip install anaouder
```

Ur wech staliet ha pa vo kinniget modeloù efedusoc'h, e c'hellit nevesaat ar meziant gant :

```bash
pip install --upgrade anaouder
```

## Adskrivañ ur restr son

Gant an urzh `adskrivan` en un terminal, e vo adskrivet ar pezh e vez komprenet gant an anaouder diouzh ur restr son. Ar wech kentañ ma vo peurgaset an urzh-se e vo ret deoc'h gortoz ur pennadig ma vefe pellkarget ha staliet ar modul `static_ffmpeg` (evit amdreiñ restroù son ha video).

```bash
adskrivan RESTR_SON_PE_VIDEO
```

Dre ziouer, adskrivet e vo pep tra e diabarzh an terminal. Gallout a rit ivez implij an opsion `-o` evit resisaat anv ur restr, e lec'h ma vo skrivet an titouroù. Tu zo implij an option-se gant an holl urzhioù eus ar meziant.

```bash
adskrivan RESTR_SON_PE_VIDEO -o DISOC'H.txt
```

Evit kaout listennad an opsionoù, implijit an opsion `-h`.

## Implijout gant ur mikro

Dre an an urzh `mikro` e c'heller implij an anaouder gant ho vouezh e amzer real.

Ma n'ez eus skrid ebet o tont, klaskit niverenn an etrefas son gant :

```bash
mikro -l
```

Ha gant an niverenn-se :

```bash
mikro -d NIVERENN_ETREFAS
```

## Linennañ ur teul skrid gant un teul son

M'ho peus un teul skrid adskrivet dre dorn (e stumm `.txt`) e c'heller linennañ ar skrid gant ar son, evit krouiñ ur restr istitloù (e stumm `srt`).

```bash
linennan RESTR_SON_PE_VIDEO RESTR_SKRID
```

## Adskrivañ istitloù evit ur video

Gallout a rit adskrivañ istitloù diouzh teuliadoù son pe video, e stumm `srt` (Subrip).

```bash
istitlan RESTR_SON_PE_VIDEO -o istitloù.srt
```

An oberiadur-se a gemero kalzig a amzer (hervez padelezh an teuliad son). Klaskit gant un teul film berr da gentañ !

https://user-images.githubusercontent.com/10166907/213805292-63becbe2-ffb5-492f-9bac-1330c4b2d07d.mp4

*Setu disoc'h an istitloù emgefre, hep cheñch netra. Kollet eo buan pa vez sonnerez...*

## Implijout gant meziantoù all

*N'eo ket aliet dre ma vez kollet un nebeut perzhioù e-keñver ar pezh vez graet gant ar modul `anaouder` : adlakaat ar varennigoù-stag hag amdreiñ an niverennoù da skouer.*

Ar model noazh a c'hellit kavout en dosser `anaouder/models` pe dre al liamm [releases](https://github.com/gweltou/vosk-br/releases).

### Audapolis

M'ho peus c'hoant implijout ar model gant ur etrefas grafikel e c'hellit mont da sellet ar raktres [Audapolis](https://github.com/bugbakery/audapolis).

### Kdenlive

Gant ar meziant frammañ videoioù [Kdenlive](https://kdenlive.org/) e c'heller adskrivañ istitloù en un doare emgefre ivez.\
Ar mod-implij a c'heller kavout [amañ](https://docs.kdenlive.org/en/effects_and_compositions/speech_to_text.html).

## Trugarez

Ar meziant-se zo bet diorroet o kemer harp war meziantoù dieub all : Kaldi, Vosk ha difazier [Hunspell](https://github.com/Drouizig/hunspell-br) an Drouizig (evit naetaat an testennoù a-raok ar pleustr).\
Lakaat da bleustriñ ar model a zo bet posubl a-drugarez d'an danvez prizius, krouet ha rannet gant ur bern tud all : ar raktres Mozilla Common Voice, enrolladennoù Dizale, Brezhoweb, RKB, Kaouen.net, Ya!, Becedia, abadennoù France3 ha Dastum.\
Trugarez da Elen Cariou, Jean-Mari Ollivier, Karen Treguier, Mélanie Jouitteau ha Pêr Morvan evit o sikour hag o souten.
