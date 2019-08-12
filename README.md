# docker-deepspeech-cy

Hyfforddi'n hwylus modelau Mozilla DeepSpeech ar gyfer adnabod lleferydd i'r Gymraeg gan defnyddio data [aml-ieithog Mozilla CommonVoice](https://voice.mozilla.org/cy/datasets) a [Chorpws Paldaruo](http://techiaith.cymru/corpora/paldaruo/)

*Easily creating Mozilla DeepSpeech models for Welsh language speech recognition using the [multi-language Mozilla CommonVoice](https://voice.mozilla.org/cy/datasets) datasets as well as the [Paldaruo Speech Corpus](http://techiaith.cymru/corpora/paldaruo/?lang=en)*

Mae'r darpariaeth yn hwyluso :
 - llwytho i lawr data hyfforddi, datblygu a phrofi
 - trosi ffeiliau sain
 
 *This package features:*
  - *downloading training, development and test data sets*
  - *conversion of audio files*

## Sut i'w ddefnyddio / *How to use*

### Derbyn URL ar gyfer data Mozilla CommonVoice / *Obtain URL for Mozilla CommonVoice data*

Wedi i chi cofrestru'ch cyfeiriad e-bost gyda Mozilla (ar https://voice.mozilla.org/cy/datasets) a derbyn e-bost sy'n cynnwys dolenni llwytho i lawr, crëwch ffeil syml o'r enw `commonvoice_url.py` o fewn [local/bin](local/bin) i gynnwys yr URL llwytho i lawr fel hyn:

*After you have registered your e-mail address with Mozilla (at https://voice.mozilla.org/cy/datasets) and receive an e-mail containing download links, create a simple file named `commonvoice_url.py` in the [local/bin](local/bin) folder to contain the base URL:*

```
!/usr/bin/env python
# -*- coding: utf-8 -*-

COMMONVOICE_DOWNLOAD_URL = 'https://common-voice-data-download.s3.amazonaws.com/........'

```

Mae modd wedyn adeiladu modelau a defnyddio'r amgylchedd docker yn llawn. 
*You can then build models and use the docker environment in full*

### Adeiladu'r amgylchedd / *Build the environment*

``` 
$ git clone https://github.com/techiaith/docker-deepspeech-cy.git
$ cd docker-deepspeech-cy
$ make
```
Bydd hyn yn achosi i'r amgylchedd adeiladu ei hun

*This will build a docker build environment.*

**D.S.** mae angen cardyn graffig â GPUs yn eich gyfrifiadur (e.e. Nvidia GeForce GTX 1080 Ti, Nvidia GeForce RTX 2080 Ti), yn ogystal a'r fersiwn diweddaraf un o [Docker](https://www.docker.com) (19.03.1, API: 1.40)

***N.B.** you will need a graphics card with GPUs on your system (e.g. Nvidia GeForce GTX 1080 Ti, Nvidia GeForce RTX 2080 Ti), as well the latest version of [Docker](https://www.docker.com) (19.03.1, API: 1.40)*



## Hyfforddi / *Training*

### Hyfforddi gyda Common Voice / *Training with Mozilla CommonVoice*


```
$ make run
root@3deb765f2438:/DeepSpeech# ./bin/bangor_welsh/import_cv_cy.py
```


### Hyfforddi gyda Paldaruo / *Training with Paldaruo*

```
$ make run
root@3deb765f2438:/DeepSpeech# ./bin/import_paldaruo.py
```
Bydd hyn yn llwytho'r corpws i lawr o techiaith.cymru . Mae'n 12G mewn maint *

*This will download the speech corpus from techiaith.cymru. It's 12Gb in size*


### Hyfforddi modelau ar gyfer cynorthwydd digidol Macsen / Training models for Macsen personal assistant 

Gweler https://techiaith.cymru/macsen

```
root@3deb765f2438:/DeepSpeech# ./bin/bangor_welsh/import_macsen.py
root@3deb765f2438:/DeepSpeech# ./bin/bangor_welsh/run-macsen.sh
```

Bydd y gorchmynion hyn yn llwytho lawr corpws benodol bach o 4 unigolyn yn darllen holl orchmynion mae Macsen yn ei adnabod, yn ogysal a chorpws llai o orchmynion Macsen ar gyfer profi.

*This will download a small development corpus of 4 individuals reading all the commands that the Macsen assistant recognizes, as well as a smaller collection of Macsen commands for testing*

Mae'r sgriptiau yn prosesu ac yn echdynnu o gorpws Macsen modelau iaith, ffeiliau trie a geirfa.

*The scripts also process and generate a language model, trie and vocabulary files. It's used in addition as a development set*


## Canlyniadau / *Results*

Gellir dod allan o'r amgylchedd docker (`exit`) wedi i'r hyfforddiant orffen a chanfod y modelau yn:

*You can `exit` the docker environment after training is completed and find models in:*

`deepspeech-docker-cy/export`

