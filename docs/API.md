# API reference

Base URL in development: `http://localhost:5000`

All request bodies are `multipart/form-data`. Error responses share the shape `{ "error": "..." }`.

---

## GET /api/health

Liveness probe. Does not load the model, so it is cheap to poll.

**200**

```json
{
  "status": "UP",
  "service": "Deepfake Speech Detection ML Service",
  "model_present": true
}
```

`model_present` is `false` when `MODEL_PATH` does not exist on disk.

---

## POST /api/predict

Classify a single audio clip.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `file` | file | yes | `wav`, `mp3`, `flac`, `ogg`, `m4a`, `webm` |

**200**

```json
{
  "classification": "Real",
  "confidence": 0.8732,
  "spectrogram": "uploads/spectrogram_5f1d9c.png"
}
```

`confidence` is the raw model output for the positive (real) class, rounded to four decimals.
`classification` is `Real` when `confidence > 0.5`, otherwise `Fake`.

**400** — no file, empty filename, or unsupported extension:

```json
{ "error": "Unsupported audio format", "allowed": ["flac", "m4a", "mp3", "ogg", "wav", "webm"] }
```

**413** — payload larger than `MAX_UPLOAD_BYTES` (20 MB default).

**503** — weights missing:

```json
{ "error": "Model not found at deepfake_audio_detection_model.h5" }
```

The uploaded file is deleted after inference, whether or not prediction succeeds.

---

## POST /transcribe

Optional speech-to-text passthrough. Returns **503** unless both `TRANSCRIBE_API_URL` and
`TRANSCRIBE_API_TOKEN` are set.

**200**

```json
{ "transcription": "..." }
```

---

## Backend (Spring Boot, port 8080)

| Method | Path | Description |
|--------|------|-------------|
| `PUT` | `/manage-account/username` | Change the authenticated user's username |
| `PUT` | `/manage-account/password` | Change the authenticated user's password |
| `POST` | `/manage-account/profile-picture` | Upload a profile picture |

These endpoints require an authenticated session; the username is taken from
`Authentication#getName()` rather than the request body.

## Limits

| Setting | Default | Environment variable |
|---------|---------|----------------------|
| Max upload | 20 MB | `MAX_UPLOAD_BYTES` |
| Sample rate | 16 kHz | — (fixed) |
| Model input | 128 × 128 × 3 | — (fixed) |
