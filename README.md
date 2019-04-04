# docker-deepspeech-cy

Hyfforddi'n hwylus modelau Mozilla DeepSpeech ar gyfer adnabod lleferydd i'r Gymraeg gan defnyddio data [aml-ieithog Mozilla CommonVoice](https://voice.mozilla.org/cy/datasets) a [Chorpws Paldaruo](http://techiaith.cymru/corpora/paldaruo/)

*Easily creating Mozilla DeepSpeech models for Welsh language speech recognition using the [multi-language Mozilla CommonVoice](https://voice.mozilla.org/cy/datasets) datasets as well as the [Paldaruo Speech Corpus](http://techiaith.cymru/corpora/paldaruo/?lang=en)*

Mae'r darpariaeth yn hwyluso :
 - llwytho i lawr data hyfforddi, datblygu a phrofi
 - rhag prosesu gan defnyddio [CorporaCreator](https://github.com/mozilla/CorporaCreator)
 - trosi ffeiliau sain
 
 *This package features:*
  - *downloading training, development and test data sets*
  - *preprocessing with [CorporaCreator](https://github.com/mozilla/CorporaCreator)*
  - *conversion of audio files*

## Sut i'w ddefnyddio / *How to use*

### Derbyn URL ar gyfer data Mozilla CommonVoice / *Obtain URL for Mozilla CommonVoice data*

Wedi i chi cofrestru'ch cyfeiriad e-bost gyda Mozilla (ar https://voice.mozilla.org/cy/datasets) a derbyn e-bost sy'n cynnwys dolenni llwytho i lawr, crëwch ffeil syml o'r enw `commonvoice_url.py` o fewn [local/bin](local/bin) i gynnwys yr URL llwytho i lawr fel hyn:

*After you have registered your e-mail address with Mozilla (at https://voice.mozilla.org/cy/datasets) and receive an e-mail containing download links, create a simple file named `commonvoice_url.py` in the [local/bin](local/bin) folder to contain the base URL:*

```
!/usr/bin/env python
# -*- coding: utf-8 -*-

COMMONVOICE_DOWNLOAD_URL_BASE = 'https://common-voice-data-download.s3.amazonaws.com/........'

```

Mae modd wedyn adeiladu modelau a defnyddio'r amgylchedd docker yn llawn. 
*You can then build models and use the docker environment in full*

### Adeiladu'r amgylchedd / *Build the environment*

``` 
$ git clone https://github.com/techiaith/docker-deepspeech-cy.git
$ cd docker-deepspeech-cy
$ make
```
Bydd hyn yn achosi i adeiladu amgylchedd docker.

*This will build a docker build environment.*

**D.S.** mae angen [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) ar eich gyfrifiadur (a chardyn â GPUs), yn ogystal a'r gyrrwyr caledwedd diweddaraf gan nvidia e.e. NVIDIA-418.56, CUDA Version: 10.1

***N.B.** you will need [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) on your system (and a graphics/GPU card) as well the latest hardware drivers from nvidia e.g. NVIDIA-418 , CUDA Version: 10.1*

## Hyfforddi / *Training*

### Hyfforddi gyda Common Voice / *Training with Mozilla CommonVoice*


```
$ make run
root@3deb765f2438:/DeepSpeech# ./bin/import_cv_cy.py
```


### Hyfforddi gyda Paldaruo / *Training with Paldaruo*

```
$ make run
root@3deb765f2438:/DeepSpeech# ./bin/import_paldaruo.py
```
Bydd hyn yn llwytho'r corpws i lawr o techiaith.cymru . Mae'n 12G mewn maint *

*This will download the speech corpus from techiaith.cymru. It's 12Gb in size*


### Hyfforddi ar gyfer Macsen / Training for Macsen 

Gweler https://techiaith.cymru/macsen

```
root@3deb765f2438:/DeepSpeech# ./bin/import_macsen.py
root@3deb765f2438:/DeepSpeech# ./bin/run-macsen.sh
```

Bydd y gorchmynion hyn yn llwytho lawr corpws benodol bach o 4 unigolyn yn darllen holl orchmynion mae Macsen yn ei adnabod, yn ogysal a chorpws llai o orchmynion Macsen ar gyfer profi.

*This will download a small development corpus of 4 individuals reading all the commands that the Macsen assistant recognizes, as well as a smaller collection of Macsen commands for testing*

Mae'r sgriptiau yn prosesu ac yn echdynnu o gorpws Macsen modelau iaith, ffeiliau trie a geirfa.

*The scripts also process and generate a language model, trie and vocabulary files. It's used in addition as a development set*


## Canlyniadau / *Results*

Gellir dod allan o'r amgylchedd docker (`exit`) wedi i'r hyfforddiant orffen a chanfod 'checkpoints' a modelau yn:

*You can `exit` the docker environment after training is completed and find checkpoints and models in:*

`deepspeech-docker-cy/homedir/.local/share/deepspeech`







