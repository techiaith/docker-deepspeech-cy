# docker-deepspeech-cy

Hwyluso hyfforddi Mozilla DeepSpeech ar gyfer adnabod lleferydd i'r Gymraeg gyda data [Mozilla CommonVoice Cymraeg](https://voice.mozilla.org/cy/datasets) a [Chorpws Paldaruo](http://techiaith.cymru/corpora/paldaruo/)

*Making it easier to train Mozilla DeepSpeech for Welsh language speech recognition using the [Welsh data in Mozilla CommonVoice](https://voice.mozilla.org/cy/datasets) datasets as well as the [Paldaruo Speech Corpus](http://techiaith.cymru/corpora/paldaruo/?lang=en)*

<br/>

#### Rhagofynion / *Pre-requisites*

 - Docker ( fersiwn/*version* >= 19)
 - cardyn graffig â GPUs yn eich gyfrifiadur (e.e. Nvidia GeForce GTX 1080 Ti, Nvidia GeForce RTX 2080 Ti) <br/>*a graphics card with GPUs on your system (e.g. Nvidia GeForce GTX 1080 Ti, Nvidia GeForce RTX 2080 Ti)*

Gweler/*See also* : https://github.com/NVIDIA/nvidia-docker#quickstart
 
<br/>
 
## Gosod / *Installation*

```
$ git clone https://github.com/techiaith/docker-deepspeech-cy
$ cd docker-deepspeech-cy
$ make
$ make run
```


### Data Cymraeg Mozilla CommonVoice / *Mozilla Common Welsh Data*

Llwythwch y data diweddaraf i lawr o https://voice.mozilla.org/cy/datasets i'r ffolder `data`.

*Download the latest data from https://voice.mozilla.org/cy/datasets to the `data`folder.


## Hyfforddi / *Training*

Gweler [README.md](local/README.md)

*See [README.md](local/README_EN.md)*
