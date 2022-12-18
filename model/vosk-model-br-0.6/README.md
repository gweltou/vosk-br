# Breton Vosk Model v6

19-11-2022

lexicon: **36 470 words** with phonemes \
corpus: **1 747 158 words**

Test "Bali Breizh er Poc'hêr : Karaez 1" : **WER 44.6%, CER 24.4%** (fastwer) \
Test Mozilla Common Voice 11 : **WER 38.1%** \
Test Baleadenn1.wav :
> "Gant ar sorserezh oa ur <del>c'harr</del> \
> Hag un <del>tammig</del> uhel ha bras"


## Train Datasets

9 785 utterances

Total audio length: **11h 48'25''** \
Male speakers: **6h 33'20''**	56% \
Female speakers: **5h 15'5''**	44% \

  * Dizale
    * Kabellig_Ruz
    * Oceanopolis
    * Nelson Mandela
    * Birmania
    * Wangari Mathai
    * Lampedusa Beach
    * Film "Ar Vreudeur Bloom"
  * Brezhoweb - Pennad Kaoz
    * Izold Guegan
    * Katell Chantreau
  * Kelaouen #Brezhoneg, Skol An Emzav
    * n° 11-12, 14-44
  * RKB
    * Atersadenn-war-eeun-Jeannot-Flaguel
    * Isabelle Caignard - Skampiola
  * Other
    * Anna Loeiza - Pemzek teiz (FR3)
  * Mozilla Common Voice 11 train set


# Test Dataset

2 351 utterances

Total audio length: **2h 33'58''** \
Male speakers: **1h 35'13''**	62% \
Female speakers: **0h 58'45''**	38% \

  * Mozilla Common Voice 11 test set


# Remarks
The corpus is augmented with 116 291 sentences from Wikipedia-br. \
The number of hidden layers was reduced from 13 to 11. \
The phonemizer was slightly improved. \
Updated Mozilla Common Voice datasets from version 7 to version 11 (which doesn't really add much audio data). \
Mozilla Common Voice train set was used for training instead of the whole "valid" set. The text of Mozilla Common Voice test set was also removed from the train corpus as it was a methodology mistake, resulting in less training data but a fair scoring.
