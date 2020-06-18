from deepspeech import Model
for i in range(5):
    ds = Model('/models/mozilla/deepspeech-0.7.3-models.pbmm')
    ds.enableExternalScorer('/models/mozilla/deepspeech-0.7.3-models.scorer')
    ds.setScorerAlphaBeta(0.75, 1.85)
    ds.__del__()
