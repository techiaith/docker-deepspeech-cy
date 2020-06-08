# docker-deepspeech-cy

Hwyluso hyfforddi Mozilla DeepSpeech ar gyfer adnabod lleferydd i'r Gymraeg gyda data [Mozilla CommonVoice Cymraeg](https://voice.mozilla.org/cy/datasets) a [Chorpws Paldaruo](http://techiaith.cymru/corpora/paldaruo/)

*Making it easier to train Mozilla DeepSpeech for Welsh language speech recognition using the [Welsh data in Mozilla CommonVoice](https://voice.mozilla.org/cy/datasets) datasets as well as the [Paldaruo Speech Corpus](http://techiaith.cymru/corpora/paldaruo/?lang=en)*

<br/>

#### Rhagofynion / *Pre-requisites*

 - Docker ( fersiwn/*version* >= 19)
 - cardyn graffig â GPUs yn eich gyfrifiadur (e.e. Nvidia GeForce GTX 1080 Ti, Nvidia GeForce RTX 2080 Ti) <br/>*a graphics card with GPUs on your system (e.g. Nvidia GeForce GTX 1080 Ti, Nvidia GeForce RTX 2080 Ti)*

Gweler/*See also* : https://github.com/NVIDIA/nvidia-docker#quickstart
 
<br/>
 
## Cychwyn arni / *Quickstart*

```
$ git clone https://github.com/techiaith/docker-deepspeech-cy
$ cd docker-deepspeech-cy
$ make
$ make run
```


### Data Cymraeg Mozilla CommonVoice / *Mozilla Common Welsh Data*

Llwythwch y data diweddaraf i lawr o https://voice.mozilla.org/cy/datasets ac yna echdynnwch popeth i ffolder newydd o dan `data`. Er enghraifft.....

*Download the latest data from https://voice.mozilla.org/cy/datasets and extract all into a new folder underneath `data`. For example.....*


```bash
techiaith@gweinydd:/home/techiaith/docker/docker-deepspeech-cy/data/commonvoice-cy-v4-20191210⟫ ls -l
total 2124544
drwxr-xr-x 2 techiaith techiaith    6459392 Feb  3 18:35 clips
-rw-r--r-- 1 techiaith techiaith     148342 Dec 10 13:42 dev.tsv
-rw-r--r-- 1 techiaith techiaith     580477 Dec 10 13:42 invalidated.tsv
-rw-r--r-- 1 techiaith techiaith    2568371 Dec 10 13:42 other.tsv
-rw-r--r-- 1 techiaith techiaith     147797 Dec 10 13:42 test.tsv
-rw-r--r-- 1 techiaith techiaith     164667 Dec 10 13:42 train.tsv
-rw-r--r-- 1 techiaith techiaith   10434562 Dec 10 13:42 validated.tsv
```

## Hyfforddi / *Training*

Y prif sgriptiau a ddefnyddir ar gyfer hyfforddi yw: 

*The sgripts primarity for training are:*

```
root@3deb765f2438:/DeepSpeech# ./bin/bangor_welsh/run-tl-cv-macsen.sh
root@3deb765f2438:/DeepSpeech# ./bin/bangor_welsh/run-tl-cv-arddweud.sh
```

Gweler y nodyn rhyddhau am wybodaeth am unrhyw ddata pellach y gallai fod eu hangen arnoch

*Please see the release note for information on any further data you might require*




