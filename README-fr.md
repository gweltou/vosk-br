[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

# Anaouder

[E brezhoneg](./README.md)

Reconnaissance vocale pour le breton avec Vosk.

## Présentation

Modèle de reconnaissance vocale (*speech-to-text*) entraîné avec le framework [Kaldi](https://www.kaldi-asr.org/), au format [Vosk](https://github.com/alphacep/vosk-api).\
Il est accompagné de scripts permettant la retranscription automatique de fichiers audio et video, l'alignement texte/son pour la création de sous-titres, ou encore l'inférence en temps réel à l'aide d'un microphone.\

Principaux avantages :

 * **Léger**. Les modèles Vosk pèsent moins de 100 Mo et peuvent tourner sur une large gamme d'appareils : ordinateurs **sans GPU**, RaspberryPi, smartphone Android...
 * **Rapide**. L'inférence se fait en **temps réel**, même sur une machine un peu datée.
 * **Local**. Fonctionne sans connexion internet. Vos données restent donc sur votre appareil.
 * **Libre et gratuit**. La licence MIT vous permet de modifier le logiciel et de l'intégrer dans d'autres applications.

Il y a toutefois des inconvénients :

 * Sensible au bruit ambiant.
 * Certains accents régionaux sont encore mal reconnus.
 * Nécessite de parler lentement et distinctement.
 * Absence de ponctuation.

Le nombre d'heures d'enregistrement audio utilisé pour entraîner le modèle est relativement faible mais progresse peu à peu.
En dehors du projet [Common Voice](https://commonvoice.mozilla.org/br) de Mozilla, les enregistrements retranscrits [libres de droit](https://creativecommons.org/licenses/) sont rares pour le breton. Toute aide sur ce terrain sera la bienvenue !

Vous pouvez également soutenir ce projet par un don financier :
[![Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/gweltou/donate)

## Installation

Les scripts nécessitent l'installation de [Python3](https://www.python.org/downloads/). L'installation du module de reconnaissance vocale se fera ensuite dans un terminal, en exécutant la commande suivante :

```bash
pip install anaouder
```

## Retranscrire un fichier audio ou video

Une fois le module installé, la commande `adskrivan` permet de retranscrire un fichier audio ou video depuis le terminal. A la première exécution de la commande, il vous faudra patienter le temps de l'installation du module `static_ffmpeg` (programme de conversion pour les fichiers audio/video). Cette installation ne se fera qu'une seule fois.

```bash
adskrivan NOM_DU_FICHIER
```

## Utilisation avec un microphone

Depuis un terminal, invoquez la commande `mikro`.

Si aucun texte n'apparaît, vous pouvez afficher la liste des interfaces audio avec la commande :

```bash
mikro -l
```

Vous pourrez ensuite préciser, en argument, le numéro de l'interface à utiliser pour l'inférence :

```bash
mikro -d NUMERO_INTERFACE
```

## Alignement d'un texte d'après un audio

Il est possible d'aligner un texte d'après un fichier audio ou video à l'aide de la commande `linennan`. Vous obtiendrez un fichier contenant le texte original, accompagné de marqueurs temporels, au format `srt` (fichier de sous-titres Subrip).\
Le fichier texte doit être un texte brut (extension `.txt`) où chaque ligne correspondra à une ligne de sous-titre.

```bash
linennan FICHIER_SON_OU_VIDEO FICHIER_TEXTE
```

Avec l'option `-o` vous pourrez préciser le nom d'un fichier d'export, par exemple :

```bash
linennan video.mp4 texte.txt -o sous-titres.srt
```

(export au format `eaf`, pour le logiciel ELAN, à venir...)

## Création automatique de sous-titres

Vous pouvez `srt` (Subrip).

```bash
istitlan FICHIER_SON_OU_VIDEO
```

## Utilisation du modèle avec d'autres logiciel 

*L'utilisation du modèle brut dans d'autres logiciel est possible mais n'est pas conseillé, puisque qu'elle omettra le post-traitement proposé par le module `anaouder` : le replacement des tirets de liaison et la normalisation-inverse des nombres notamment.*

Le modèle brut est accessible sous le dossier `anaouder/models` ou par le lien "[releases](https://github.com/gweltou/vosk-br/releases)".

### Kdenlive

Le logiciel de montage video [Kdenlive](https://kdenlive.org/) permet l'utilisation de modèles Vosk pour la retranscription automatique de sous-titres.\
Voir la [documentation](https://docs.kdenlive.org/en/effects_and_compositions/speech_to_text.html).
