# Sgriptiau Hyfforddi DeepSpeech Mozilla

*Click [here](README_EN.md) to read this page in English*

Mae dogfennaeth gan Mozilla ar DeepSpeech ar gael fan hyn: https://deepspeech.readthedocs.io 

Mae'r sgriptiau canlynol yn cysylltu ag yn hwyluso'r holl gamau a ddilynir er mwyn hyfforddi, gynhyrchu a gwerthuso modelau adnabod lleferydd Cymraeg gyda DeepSpeech Mozilla. Defnyddir setiau Cymraeg o wefan CommonVoice Mozilla fel prif ffynhonnell data hyfforddi. Gydag adnoddau bellach gan Uned Technolegau Iaith, Prifysgol Bangor, mae'r modelau'n addas ar gyfer rhaglenni cynorthwyydd digidol (e.e. Macsen) a thrawsgrifiwr gyffredinol. 


## Rhagofynion

Llwythwch i lawr data lleferydd Cymraeg o wefan CommonVoice: https://voice.mozilla.org/cy/datasets sy'n cael ei ddarparu fel un ffeil mawr wedi'i gwasgu (e.e. `cy.tar.gz`) . Cadwch y ffeil o fewn y ffolder `data`. 


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

Defnyddiwch y sgript ganlynol i hyfforddi model acwstig. Dyle paramedr `-a` nodi ble mae'r ffeiliau CSV o ganlyniad i fewnforio CommonVoice. Yn yr enghraifft hon, maent wedi'u lleoli yn is-gyfeiriadur `/clips` y `target_dir` gwreiddiol.

### `run_tl_cv_cy.sh`

```shell
root@c67722092f2e:/DeepSpeech# /DeepSpeech/bin/bangor_welsh/run_tl_cv_cy.sh -c /data/commonvoice-cy-v4-20191210/clips
```

Mae'r sgript hon yn defnyddio nodwedd dysgu trosglwyddol (*transfer learning*) DeepSpeech er mwyn cael rhywfaint o fudd o ddefnyddio modelau iaith Saesneg Mozilla, sydd wedi'u hyfforddi ar gasgliadau data llawer mwy, fel man cychwyn ar gyfer hyfforddi adnabod lleferydd Cymraeg.

## Modelau Iaith / Parth Penodol

Nid yw model acwstig ar ei ben ei hun, er ei fod wedi defnyddio technegau dysgu trosglwyddo, yn ddigonol ar gyfer adnabod lleferydd Cymraeg effeithiol. Mae model iaith yn cynorthwyo peiriant adnabod lleferydd i gynhyrchu nid yn unig geiriau dilys (o ddilyniannau ffonemau) ond hefyd ddilyniannau mwy dilys o eiriau.

### `import_bangor_resources.py`

Mae angen rhagor o adnoddau gan Brifysgol Bangor er mwyn hyfforddi DeepSpeech ar gyfer adnabod lleferydd Cymraeg mewn gwahanol gyd-destunau defnyddiol. 

Mae'r sgript isod yn llwytho i lawr rhagor o recordiadau a/neu corpora testun sydd yn galluogi adnabod lleferydd Cymraeg o fewn cynorthwyydd digidol ('macsen') neu drawsgrifiwr ('transcribe') (fel yr ofynnir ym mharamedr `-d`)

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/import_bangor_resources.py -t /data/macsen -d macsen
```

### `clean_lm_corpus.py`

Y cam angenrheidiol cyntaf ar gyfer paratoi modelau iaith yw i glanhau'r ffynhonnell drwy eithrio unrhyw destunau fyddai'n tanseilio model effeithiol ac adnabod lleferydd. e.e. brawddegau sy'n cynnwys rhifau neu nodau nad ydynt o fewn ein gwyddor.

Mae'r adnoddau Macsen a Thrawsgrifydd yn cynnwys ffeil `corpus.txt` sy'n cynnwys enghreifftiau o frawddegau dilys yn eu priod feysydd. Ar ôl rhedeg y sgript hon dylai fod gennych ffeil `corpus.clean.txt` yn yr un cyfeiriadur a'r ffeil ffynhonnell.

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/clean_lm_corpus.py -s /data/macsen/corpus.txt -o /data/macsen/corpus.clean.txt 
```

### `build_lm_scorer.sh`

Dyma'r brif sgript ar gyfer hyfforddi model iaith. Os rhoddir set profi adnabod lleferydd (fel y nodir gyda `-t`), yna bydd y sgript yn arbrofi gyda wahanol paramedrau modelau iaith nes iddo dod o hyd i'r gwerthoedd gorau posibl sy'n rhoi'r cyfraddau gwallau adnabod lleferydd isaf posibl.
 
Gall y broses gymryd amser hir - oriau neu ddiwrnod neu ddau - gan y bydd yn arbrofi filoedd o weithiau. Yn y diwedd, bydd y sgript yn adrodd ar ddau werth gorau posibl ac yn gofyn ichi eu mewnbynnu i'w cynnwys ym mhecyn terfynol y model iaith. (gweler y ffeil `kenlm.scorer` yn y cyfeiriadur a bennir gan y ddadl sgript` -o`)

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/build_lm_scorer.sh -s /data/macsen/corpus.clean.txt -o /data/macsen/ -t /data/macsen/deepspeech.csv
```

### `evaluate_lm_scorer.sh`

Gallwch ddefnyddio'r sgript ganlynol i ddarparu gwerthusiad o'ch modelau.

```shell
root@6a88b0d59848:/DeepSpeech# bin/bangor_welsh/evaluate_lm_scorer.sh -l /data/mascen -t /data/macsen/deepspeech.csv
```
