# Model card — deepfake speech classifier

## Overview

A convolutional classifier that labels a short audio clip as **Real** or **Fake** (synthetic
speech). It is served by the Flask service in `ml-service/`.

## Input

| Property | Value |
|----------|-------|
| Sample rate | 16 kHz, mono |
| Features | 13 MFCC coefficients |
| Tensor | `1 × 128 × 128 × 3` (MFCC matrix resized and stacked across 3 channels) |
| File formats | wav, mp3, flac, ogg, m4a, webm |
| Max size | 20 MB |

## Output

A single sigmoid score in `[0, 1]`:

- `score > 0.5` → **Real**
- `score <= 0.5` → **Fake**

The API returns the score as `confidence`. It is *not* calibrated, so it should be read as a
relative signal rather than a probability you can act on in isolation.

## Architecture

Keras CNN (`deepfake_audio_detection_model.h5`). The weights file is not committed; see the
README for how to obtain it. `preprocessing.py` contains the exact feature pipeline used at
inference time, so training and serving stay in sync.

## Intended use

- Research and coursework on synthetic-speech detection.
- A demonstration of end-to-end ML deployment (React → Flask → Keras).

## Out of scope

- Production moderation or identity verification.
- Legal, forensic or journalistic conclusions.
- Languages and recording conditions not represented in the training data.
- Detecting partially manipulated audio, music beds, or heavy background noise.

## Limitations

- The MFCC resize to `128 × 128` discards fine time-frequency detail; very short or very long
  clips may behave inconsistently.
- Performance depends on the codec and sample rate of the input; heavily compressed uploads
  degrade accuracy.
- Newer synthesis models may not be represented in the training distribution.
- No calibration step is applied, so the threshold of `0.5` is a convention, not a tuned
  operating point.

## Evaluation

The repository does not currently ship a recorded evaluation report. To reproduce metrics,
run the held-out clips through `preprocess_input_audio` + the model and compute accuracy,
precision/recall and ROC-AUC. Adding `docs/EVALUATION.md` with the resulting numbers is the
next step before quoting performance anywhere.

## Ethical notes

Deepfake detection is adversarial: a `Fake` verdict is a signal, not proof. Present results
with the confidence score and encourage human review.
