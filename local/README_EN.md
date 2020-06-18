# Scripts for Training Mozilla DeepSpeech

*Cliciwch [yma](README.md) i ddarllen y dudalen hon yn Gymraeg*

Documentation by Mozilla on DeepSpeech can be found here: https://deepspeech.readthedocs.io 

The following scripts demonstrate how the general steps described in Mozilla's documentation can be used to create Welsh language speech recognition models for both a voice assistant (e.g. Macsen) and a transcribing applications. 


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

### `run_tl_cv_cy.sh`

```shell
root@c67722092f2e:/DeepSpeech# /DeepSpeech/bin/bangor_welsh/run_tl_cv_cy.sh -c /data/commonvoice-cy-v4-20191210/clips
```

## Language Models / Domain Specific

### `import_bangor_resources.py`

You will need further resources from Bangor University in order to train  DeepSpeech for various Welsh language applications. The below script will download further recordings and/or text corpora that facilitate Welsh speech recognition for a simple voice assistant ('macsen') or a transcriber ('transcribe').

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/import_bangor_resources.py -t /data/macsen -d macsen
```

### `clean_lm_corpus.py`

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/clean_lm_corpus.sh -s /data/texts/macsen/corpus.txt -o /data/texts/macsen/corpus.clean.txt 
```

### `build_lm_scorer.sh`

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/build_lm_scorer.sh -s /data/texts/macsen/corpus.clean.txt -o /data/texts/macsen/ -t /data/macsen/deepspeech.csv
```

### `evaluate_lm_scorer.sh`

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/evaluate_lm_scorer.sh -l /data/texts/macsen -t /data/macsen/deepspeech.csv
```
