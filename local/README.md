# Sgriptiau Hyfforddi DeepSpeech Mozilla

*Click [here](README_EN.md) to read this page in English*

## Rhagofynion

Data Cymraeg gan o wefan CommonVoice: https://voice.mozilla.org/cy/datasets


## Paratoi Data

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

## Model Acwstig

### `run_tl_cv_cy.sh`

 * [ ] - tynnu allan paths 'hardcoded'

```shell
root@c67722092f2e:/DeepSpeech# /DeepSpeech/bin/bangor_welsh/run_tl_cv_cy.sh
```


## Modelau Iaith / Parth Penodol

### Estyn adnoddau Macsen

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/import_audio_macsen.py -t /data/macsen
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
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/evaluate_lm_scorer.sh -l /data/texts/mascen -t /data/macsen/deepspeech.csv
```
