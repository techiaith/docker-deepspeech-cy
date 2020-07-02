# Scripts for Training Mozilla DeepSpeech

*Cliciwch [yma](README.md) i ddarllen y dudalen hon yn Gymraeg*

Documentation by Mozilla on DeepSpeech can be found here: https://deepspeech.readthedocs.io 

The following scripts join up all the steps that are needed to train, generate and evaluate models for Welsh language speech recognition with Mozilla's DeepSpeech. The Welsh datasets from Mozilla's CommonVoice website are the primary resource for training. With some further resources from Bangor University's Language Technologies Unit, the models are viable for voice assistant (e.g. Macsen) and a transcriber applications. 


## Prerequisites

Download the Welsh speech data from the Mozilla CommonVoice website: https://voice.mozilla.org/cy/datasets which is provided as a single large compressed file (`.tar.gz`). Save the file into the `data` ffolder. 


## Prepare Data

### `import_audio_archive.py`

```shell
root@c67722092f2e:/DeepSpeech# bin/bangor_welsh/import_audio_archive.py --archive /data/cy-v4.tar.gz --target_dir /data/commonvoice-cy-v4-20191210/
```

### `analyze_audio.py`

```shell
root@c67722092f2e:/DeepSpeech# /DeepSpeech/bin/bangor_welsh/analyze_audio.py --csv_dir /data/commonvoice-cy-v4-20191210/clips/
/data/commonvoice-cy-v4-20191210/clips/dev.csv                0.91 hours      (3269.93 seconds)
/data/commonvoice-cy-v4-20191210/clips/test.csv               0.98 hours      (3514.49 seconds)
/data/commonvoice-cy-v4-20191210/clips/train.csv              1.09 hours      (3941.04 seconds)
/data/commonvoice-cy-v4-20191210/clips/train-all.csv          7.48 hours      (26928.55 seconds)
/data/commonvoice-cy-v4-20191210/clips/other.csv              14.75 hours     (53092.44 seconds)
/data/commonvoice-cy-v4-20191210/clips/validated.csv          58.16 hours     (209380.97 seconds)
```


## Acoustic Model

Use the following script to train an acoustic model. The `-a` argument needs to point to where to the CSV files from your CommonVoice import. In this example, they are located in the `/clips` subdirectory of the original `target_dir`.  

### `run_tl_cv_cy.sh`

```shell
root@c67722092f2e:/DeepSpeech# /DeepSpeech/bin/bangor_welsh/run_tl_cv_cy.sh -a /data/commonvoice-cy-v4-20191210/clips
```

This script uses DeepSpeech's transfer learning feature in order to derive some benefit from using Mozilla's English language models, trained on much larger data collections, as a starting point for training Welsh speech recognition.



## Language Models / Domain Specific

An acoustic model on its own, despite having used transfer learning techniques, is insufficient for effective speech recognition. A language model aids the speech recognition in producing not only what are valid words (from phoneme sequences) but also more valid sequences of words. 


### `import_bangor_resources.py`

You will need further resources from Bangor University in order to train  DeepSpeech with language models for various Welsh language applications. 

The following script will download further recordings and/or text corpora that facilitate Welsh speech recognition for a simple voice assistant ('macsen') or a transcriber ('transcribe') (as requested in the `-d` argument).

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/import_bangor_resources.py -t /data/macsen -d macsen
```

### `clean_lm_corpus.py`

The first necessary step for preparing language models is for sources to be cleaned of any texts that would undermine an effective model and speech recognition. e.g. numbers or character not within our pre-defined alphabet.

Both Macsen and Transcriber resources contain a `corpus.txt` file that contain examples of valid sentences in their respective domains. After running this script you should have a `corpus.clean.txt` file in the same directory. 


```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/clean_lm_corpus.py -s /data/texts/macsen/corpus.txt -o /data/texts/macsen/corpus.clean.txt 
```

### `build_lm_scorer.sh`

This is the main script for training a language model. If a test set for recognition (as indicated with `-t` ) is given, the script will experiment with various language model parameters until it finds optimal values that give the lowest possible recognition error rates. 
 
The process can take a long time - hours or possibly day or two - since it will experiment many thousands of times. In the end, the script will report on two optimal values and ask you to enter them for final inclusion in the finally packaged language model. (`kenlm.scorer` in the directory specified by the `-o` script argument)

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/build_lm_scorer.sh -s /data/texts/macsen/corpus.clean.txt -o /data/texts/macsen/ -t /data/macsen/deepspeech.csv
```

### `evaluate_lm_scorer.sh`

You can use the following script to provide an evaluation of your models. 

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/evaluate_lm_scorer.sh -l /data/texts/macsen -t /data/macsen/deepspeech.csv
```
