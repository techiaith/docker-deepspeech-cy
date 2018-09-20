# docker-deepspeech-cy

Datblygu creu modelau Mozilla DeepSpeech ar gyfer adnabod lleferydd i'r Gymraeg gan defnyddio data [Corpws Paldaruo](http://techiaith.cymru/corpora/paldaruo/)

*Developing for creating Mozilla DeepSpeech models for Welsh language speech recognition using the [Paldaruo Speech Corpus](http://techiaith.cymru/corpora/paldaruo/?lang=en)*

## Sut i'w ddefnyddio / How to use

``` 
$ git clone https://github.com/dewibrynjones/docker-deepspeech-cy.git
$ cd docker-deepspeech-cy
$ make
```
Bydd hyn yn achosi i adeiladu amgylchedd docker.
*This will build a docker build environment.*

**D.S.** mae angen [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) ar eich gyfrifiadur (a chardyn â GPUs)
***N.B.** you will need [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) on your system (and a graphics/GPU card)*

Yna / *and then*:

```
$ make run
root@3deb765f2438:/DeepSpeech# ./bin/import_paldaruo.py
```
Bydd hyn yn llwytho'r corpws i lawr o techiaith.cymru . Mae'n 12G mewn maint *
*This will download the speech corpus from techiaith.cymru. It's 12Gb in size*

## Hyfforddi ar gyfer Macsen / Training for Macsen 

Gweler https://techiaith.cymru/macsen

```
root@3deb765f2438:/DeepSpeech# ./bin/import_testset_macsen.py
root@3deb765f2438:/DeepSpeech# ./bin/run-macsen.sh
```

Bydd y gorchmynion hyn yn llwytho lawr corpws profi bach o 4 unigolyn yn darllen holl orchmynion mae Macsen yn ei adnabod. 

*This will download a small test corpus of 4 individuals reading all the commands that the Macsen assistant recognizes*

Mae'r sgriptiau yn prosesu ac yn echdynnu o gorpws Macsen modelau iaith, ffeiliau trie a geirfa. Fe defnyddir yn ogystal fel set datblygu.

*The scripts also process and generate a language model, trie and vocabulary files. It's used in addition as a development set*



# HEN HANES ~ OUT OF DATE #

## Canlyniadau cychwynol / Initial results

RHYBYDD : mae angen mwy o waith i ddileu'r negeseuon gwall ac er mwyn wireddu hyfforddi a profi cywir. Hyd yn hyn, mae'r canlyniadau isod ond yn cadarnhau bod y sgriptiau mewnforio yn gweithio. 

*WARNING : more work is needed to eliminate error messages and for correct training and testing. At this stage, the below results indicate that the import script works.*

```
root@3deb765f2438:/DeepSpeech# ./bin/run-paldaruo.sh 
Error: Mismatching alphabet size in trie file and alphabet file. Trie file will not be loaded.
WARNING:tensorflow:It seems that global step (tf.train.get_global_step) has not been increased. Current value (could be stable): 14595 vs previous value: 14595. You could increase the global step by passing tf.train.get_global_step() to Optimizer.apply_gradients or Optimizer.minimize.
WARNING:tensorflow:It seems that global step (tf.train.get_global_step) has not been increased. Current value (could be stable): 14595 vs previous value: 14595. You could increase the global step by passing tf.train.get_global_step() to Optimizer.apply_gradients or Optimizer.minimize.

...

I Test of Epoch 15 - WER: 0.088874, loss: 1.1484046695813277, mean edit distance: 0.012831
I --------------------------------------------------------------------------------
I WER: 0.083333, loss: 0.003980, mean edit distance: 0.018519
I  - src: "ar y cefn ac roedd nesaf i gyd doedd dim cynnwys amlwg"
I  - res: "a y cefn ac roedd nesaf i gyd doedd dim cynnwys amlwg"
I --------------------------------------------------------------------------------
I WER: 0.153846, loss: 0.004407, mean edit distance: 0.017857
I  - src: "dosbarth yr un fod yn fawr ni yr ysgol ail ganrif am nid"
I  - res: "dosbarth yr un fodyn fawr ni yr ysgol ail ganrif am nid"
I --------------------------------------------------------------------------------
I WER: 0.181818, loss: 0.002747, mean edit distance: 0.016949
I  - src: "datblygu ac ati traddodiad yn byw ond hefyd y dydd williams"
I  - res: "datblygu ac ati traddodiad yn byw ond hefyd y dyddwilliams"
I --------------------------------------------------------------------------------
I WER: 0.181818, loss: 0.003672, mean edit distance: 0.017544
I  - src: "i ddod cyngor athrawon bychan neu digwydd hud mynd i weld"
I  - res: "i ddodcyngor athrawon bychan neu digwydd hud mynd i weld"
I --------------------------------------------------------------------------------
I WER: 0.200000, loss: 0.003280, mean edit distance: 0.016667
I  - src: "amgylchiadau gweithwyr fy mam ac yn llogi pethau unrhyw drws"
I  - res: "amgylchiadau gweithwyr fy mam ac yn llogi pethau unrhywdrws"
I --------------------------------------------------------------------------------
I WER: 0.222222, loss: 0.004084, mean edit distance: 0.016949
I  - src: "dros y ffordd gwasanaeth byddai'r rhestr hyd llygaid lloegr"
I  - res: "dros y ffordd gwasanaeth byddai'r rhestr hydllygaid lloegr"
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 0.002930, mean edit distance: 0.017857
I  - src: "gwraig oren diwrnod gwaith mewn eisteddfod disgownt iddo"
I  - res: "gwraig oren diwrnod gwaith mewn eisteddfoddisgownt iddo"
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 0.004063, mean edit distance: 0.017857
I  - src: "gwraig oren diwrnod gwaith mewn eisteddfod disgownt iddo"
I  - res: "gwraig oren diwrnod gwaith mewn eisteddfoddisgownt iddo"
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 0.004414, mean edit distance: 0.016949
I  - src: "oherwydd elliw awdurdod blynyddoedd gwlad tywysog llyw uwch"
I  - res: "oherwydd elliw awdurdodblynyddoedd gwlad tywysog llyw uwch"
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 0.004554, mean edit distance: 0.024390
I  - src: "gwneud iawn un dweud llais wedi gyda llyn"
I  - res: "gwneud iawn un dweudllais wedi gyda llyn"
I --------------------------------------------------------------------------------
```

Gellir dod allan o'r amgylchedd docker (`èxit`) wedi i'r hyfforddiant orffen a chanfod 'checkpoints' a modelau yn:
*You can `èxit` the docker environment after training is completed and find checkpoints and models in:*

`deepspeech-docker-cy/homedir/.local/share/deepspeech`







