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



## Canlyniadau cychwynol / Initial results

RHYBUDD : mae angen mwy o ddata i wella'r canlyniadau WER ac i gynyddu'r nifer o eiriau a brawddegau a adnabyddir. 

*WARNING : more data is needed to improve WER results and to increase the amount of recognised words and sentences.*

```
root@4f7dc831e857:/DeepSpeech# ./bin/run-macsen.sh 
('Preprocessing', ['/data/paldaruo/deepspeech.csv'])
Preprocessing done
('Preprocessing', ['/data/testsets/macsen/deepspeech.csv'])
Preprocessing done
('Preprocessing', ['/data/testsets/macsen/deepspeech.csv'])
Preprocessing done
I STARTING Optimization
I Training epoch 0...
I Training of Epoch 0 - loss: 191.818658                                                                                                                                                                                                                                 
100% (973 of 973) |################################################################################################################################################################################################################| Elapsed Time: 0:18:36 Time:  0:18:36
I Training epoch 1...
I Training of Epoch 1 - loss: 172.296847                                                                                                                                                                                                                                 
100% (973 of 973) |################################################################################################################################################################################################################| Elapsed Time: 0:18:51 Time:  0:18:51
I Training epoch 2...
I Training of Epoch 2 - loss: 102.362789                                                                                                                                                                                                                                 
100% (973 of 973) |################################################################################################################################################################################################################| Elapsed Time: 0:18:51 Time:  0:18:51
I Training epoch 3...
I Training of Epoch 3 - loss: 34.322051                                                                                                                                                                                                                                  
100% (973 of 973) |################################################################################################################################################################################################################| Elapsed Time: 0:18:47 Time:  0:18:47
I Training epoch 4...
I Training of Epoch 4 - loss: 12.262248                                                                                                                                                                                                                                  
100% (973 of 973) |################################################################################################################################################################################################################| Elapsed Time: 0:20:00 Time:  0:20:00
I Training epoch 5...
I Training of Epoch 5 - WER: 0.153180, loss: 6.594689672493126, mean edit distance: 0.047680                                                                                                                                                                             
I --------------------------------------------------------------------------------
I WER: 0.090909, loss: 0.224085, mean edit distance: 0.018519
I  - src: "cynllun cychwyn diolch llyfr yn y blaen dan i ddim cyn"
I  - res: "cynllun cychwyn diolch llyfr yn y blaen dan i ddim cy"
I --------------------------------------------------------------------------------
I WER: 0.090909, loss: 0.232132, mean edit distance: 0.018519
I  - src: "cynllun cychwyn diolch llyfr yn y blaen dan i ddim cyn"
I  - res: "cynllun cychwyn diolch llyfr yn y blaen dan i ddim cy"
I --------------------------------------------------------------------------------
I WER: 0.090909, loss: 0.288061, mean edit distance: 0.018519
I  - src: "cynllun cychwyn diolch llyfr yn y blaen dan i ddim cyn"
I  - res: "cynllun cychwyn diolch llyfr yn y blaen dan i ddim cy"
....
```

```
100% (973 of 973) |###############################################################################################################################################################################################################| Elapsed Time: 12:24:29 Time: 12:24:29
I Validating epoch 5...
I Validation of Epoch 5 - WER: 0.981913, loss: 103.99932567889874, mean edit distance: 0.724353                                                                                                                                                                          
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 25.771280, mean edit distance: 0.250000
I  - src: "distawa "
I  - res: "distaw"
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 25.771280, mean edit distance: 0.250000
I  - src: "distawa "
I  - res: "distaw"
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 26.369864, mean edit distance: 0.625000
I  - src: "distawa "
I  - res: "daw"
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 26.369864, mean edit distance: 0.625000
I  - src: "distawa "
I  - res: "daw"
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 27.724842, mean edit distance: 0.285714
I  - src: "macsen "
I  - res: "masan "
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 27.724842, mean edit distance: 0.285714
I  - src: "macsen "
I  - res: "masan "
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 32.695435, mean edit distance: 0.625000
I  - src: "distawa "
I  - res: "isowod"
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 32.695435, mean edit distance: 0.625000
I  - src: "distawa "
I  - res: "isowod"
I --------------------------------------------------------------------------------
I WER: 2.000000, loss: 33.126911, mean edit distance: 0.571429
I  - src: "macsen "
I  - res: "smas n"
I --------------------------------------------------------------------------------
I WER: 2.000000, loss: 33.126911, mean edit distance: 0.571429
I  - src: "macsen "
I  - res: "smas n"
I --------------------------------------------------------------------------------
100% (13 of 13) |##################################################################################################################################################################################################################| Elapsed Time: 0:01:49 Time:  0:01:49
I Training epoch 6...
I Training of Epoch 6 - loss: 4.346718     
```

Gellir dod allan o'r amgylchedd docker (`exit`) wedi i'r hyfforddiant orffen a chanfod 'checkpoints' a modelau yn:

*You can `exit` the docker environment after training is completed and find checkpoints and models in:*

`deepspeech-docker-cy/homedir/.local/share/deepspeech`







