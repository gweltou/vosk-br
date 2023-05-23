# Breton Vosk Model v7

19-11-2022

lexicon: **43 468 words** with phonemes \
corpus: **2 862 007 words**

Test "Bali Breizh er Poc'hêr : Karaez 1" : **WER 42.5%, CER 23.7%** (fastwer) \
Test Mozilla Common Voice 11 : **WER 36.4%** \
Test Baleadenn1.wav :
> "Gant ar sorserezh oa ur <del>c'harr</del> \
> Hag un <del>tammig</del> uhel ha bras"


## Train Datasets

10 647 utterances

- Total audio length:	**13h 19' 54''** \
- Male speakers:	**7h 28' 8''**	56.0% \
- Female speakers:	**5h 51' 46''**	44.0% \

 * aligned/ya!/900/900-p_3-pignat-tour-tan-Eckmülh
 * aligned/ya!/900/900-p_3-Ger-ar-pennskridaozer-nevez
 * aligned/ya!/900/900-p_4-An-takad-tenn
 * aligned/dizale/Kabellig_Ruz/Kabellig_Ruz
 * aligned/dizale/filmou/Ar_Vreudeur_Bloom
 * aligned/dizale/Oceanopolis/Oceanopolis
 * aligned/dizale/Birmania/Birmania_Mouezh
 * aligned/dizale/Wangari_Maathai/Wangari_Maathai_Bob_Nolwenn
 * aligned/dizale/Mandela/Mandela_Bob_Nolwenn
 * aligned/dizale/Lampedusa/Lampedusa_Beach_22122016
 * aligned/RKB/211026-Atersadenn-war-eeun-Jeannot-Flaguel
 * aligned/RKB/PLANT-s11-ISABELLE-CAIGNARD-SKAMPIOLA
 * aligned/RKB/al_linad_gant_isabelle_39469393-1dab-4793-9722-ab85655a812b
 * aligned/RKB/ar_penn-ognon_gant_isabelle_caignard_f3c24c8d-4d6a-484d-85be-6f4787305c2d
 * aligned/brezhoweb/Choarioù_video_e_brezhoneg_Streamer_en_breton_🎮_-_YouTube
 * aligned/brezhoweb/pennad_kaoz/PENNAD_KAOZ_KATELL_CHANTREAU
 * aligned/brezhoweb/pennad_kaoz/PENNAD_KAOZ_IZOLD_GUEGAN
 * aligned/Mélanie/Janig_I_II
 * aligned/dastum/Intañv_al_lochenn_a73552
 * aligned/dastum/an_otroumobil_524Y00030-11
 * aligned/MCV11/37350e73c62e7ba5/37350e73c62e7ba5
 * aligned/MCV11/d6ac3dfc34f06ac4/d6ac3dfc34f06ac4
 * aligned/MCV11/520a2dece2442a0d/520a2dece2442a0d
 * aligned/MCV11/ccdf026db3b4f0a0/ccdf026db3b4f0a0
 * aligned/MCV11/3b01294e488a1e83/3b01294e488a1e83
 * aligned/MCV11/0936399255af8057/0936399255af8057
 * aligned/MCV11/9aae8bca0439226f/9aae8bca0439226f
 * aligned/#brezhoneg/b23/b23
 * aligned/#brezhoneg/b29/b29
 * aligned/#brezhoneg/b35/b35
 * aligned/#brezhoneg/b21/b21
 * aligned/#brezhoneg/b37/b37
 * aligned/#brezhoneg/b34/b34
 * aligned/#brezhoneg/b42/b42
 * aligned/#brezhoneg/b41/b41
 * aligned/#brezhoneg/b39/b39
 * aligned/#brezhoneg/b11/b11
 * aligned/#brezhoneg/b43/b43
 * aligned/#brezhoneg/b32/b32
 * aligned/#brezhoneg/b27/b27
 * aligned/#brezhoneg/b30/b30
 * aligned/#brezhoneg/b36/b36
 * aligned/#brezhoneg/b13/b13
 * aligned/#brezhoneg/b14/b14
 * aligned/#brezhoneg/b28/b28
 * aligned/#brezhoneg/b15/b15
 * aligned/#brezhoneg/b25/b25
 * aligned/#brezhoneg/b12/b12
 * aligned/#brezhoneg/b18/b18
 * aligned/#brezhoneg/b33/b33
 * aligned/#brezhoneg/b26/b26
 * aligned/#brezhoneg/b17/b17
 * aligned/#brezhoneg/b16/b16
 * aligned/#brezhoneg/b44/b44
 * aligned/#brezhoneg/b31/b31
 * aligned/#brezhoneg/b24/b24
 * aligned/#brezhoneg/b40/b40
 * aligned/#brezhoneg/b22/b22
 * aligned/#brezhoneg/b19/b19
 * aligned/#brezhoneg/b20/b20
 * aligned/#brezhoneg/b38/b38
 * aligned/FR3/anna_loeiza_pemzek_teiz
 * aligned/becedia/becedia_suzanne_goarnisson_scrignac
 * aligned/kaouenn/trugarez_tad_trugarez_mamm
 * aligned/kaouenn/arouez_an_evned_b9e9b12755d8349e76fb1a1f56759b56
 * aligned/kaouenn/noz_an_nedeleg_yf_kemener_6398ee99ad216a2992af353f9313c68a
 * aligned/kaouenn/an_tad_michel_jaouen_3109ac50477be39dc2cf27e4994d4237
 * aligned/kaouenn/filip_neri_dc978d84b913c8d87c80b4da19a3c30b
 * aligned/kaouenn/noz_kalana_997e41c2016afe4338977389ba65c6a9
 * aligned/YBD/rann1


# Test Dataset

2 101 utterances

- Total audio length:	**2h 0' 11''** \
- Male speakers:	**1h 19' 47''**	66.4% \
- Female speakers:	**0h 40' 24''**	33.6% \

 * Mozilla Common Voice 11 test set


# Remarks

The corpus is augmented with 216,389 sentences from Wikipedia-br and Ya!. \
The number of hidden layers was reduced from 13 to 11. \
First model trained on a GPU (Geforce GTX 1060) for around 7h.
