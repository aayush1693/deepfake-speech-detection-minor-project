# 🎙️ Deepfake Speech Detection

A full-stack system for detecting AI-generated (deepfake) speech. Users upload an audio clip,
a TensorFlow model classifies it as **Real** or **Fake**, and the frontend shows the confidence
score alongside a spectrogram of the clip. The same repo also hosts the account layer
(registration, login, profile management) used by the dashboard.

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 17, Material UI, `react-dropzone`, axios |
| Backend | Spring Boot 3.4, Spring Security, JPA, Liquibase-style SQL schema, MySQL |
| ML service | Flask, TensorFlow/Keras, librosa, NumPy |
| Infra | Docker Compose, GitHub Actions |

## Architecture

```
React (3000)  ──►  Flask ML service (5000)  ──►  Keras CNN
     │                     │
     └──►  Spring Boot (8080)  ──►  MySQL
                accounts, profile pictures, OTP
```

The React client talks to the Flask service for audio analysis and to the Spring Boot service
for authentication and account management.

## Repository layout

```
.
├── frontend/            React client
│   └── src/services/    API client used by the pages
├── backend/             Spring Boot account service
│   └── src/main/java/com/deepfake/backend/
├── ml-service/          Flask inference API
│   ├── app.py           HTTP routes
│   ├── preprocessing.py MFCC + spectrogram helpers
│   └── validators.py    request validation
└── docker-compose.yml
```

## How detection works

1. `librosa` loads the clip at 16 kHz mono.
2. 13 MFCC coefficients are computed, resized to `128 × 128` and stacked across 3 channels
   to match the CNN input.
3. The Keras model returns a score in `[0, 1]`; values above `0.5` are labelled **Real**,
   otherwise **Fake**.
4. A log-frequency spectrogram of the clip is rendered and saved for the UI.

### Model weights

The trained weights (`ml-service/deepfake_audio_detection_model.h5`, ~85 MB) are **not
versioned** — see `.gitignore`. To run inference, place the file at
`ml-service/deepfake_audio_detection_model.h5` or point `MODEL_PATH` at it.

The service still starts without the weights: `/api/health` reports `model_present: false`
and `/api/predict` returns `503` with a clear message.

## Getting started

### 1. Configuration

```bash
cp .env.example .env
# fill in MAIL_*, DB_* and (optionally) TRANSCRIBE_*
```

Credentials are read from the environment. Nothing secret is committed.

### 2. ML service

```bash
cd ml-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py            # http://localhost:5000
```

### 3. Backend

```bash
cd backend
mysql -u root -p < src/main/resources/schema.sql
mvn spring-boot:run      # http://localhost:8080
```

### 4. Frontend

```bash
cd frontend
npm install
npm start                # http://localhost:3000
```

Set `REACT_APP_API_URL` if the ML service is not on the same origin.

### Or run everything with Docker

```bash
docker compose up --build
```

## API

### `GET /api/health`

```json
{ "status": "UP", "service": "Deepfake Speech Detection ML Service", "model_present": true }
```

### `POST /api/predict`

Multipart upload with a single `file` field. Accepted formats: `wav`, `mp3`, `flac`, `ogg`,
`m4a`, `webm` (max 20 MB).

```json
{
  "classification": "Fake",
  "confidence": 0.9134,
  "spectrogram": "uploads/spectrogram_9f2c....png"
}
```

### `POST /transcribe`

Optional passthrough endpoint. Disabled (`503`) unless `TRANSCRIBE_API_URL` and
`TRANSCRIBE_API_TOKEN` are configured.

## Tests

```bash
cd ml-service
pip install -r requirements-dev.txt
pytest -q
```

Validator tests run with no ML dependencies; preprocessing tests are skipped automatically
when `librosa` is unavailable.

## Security notes

- The SMTP and MySQL credentials that were previously hardcoded in
  `application.properties` and the Flask OTP helper have been removed and now come from
  the environment. **Rotate any credential that was ever committed.**
- Uploads are stored under a generated filename and deleted after inference.
- OTPs are six digits and short-lived by design; the mail sender must be configured before
  `send_otp` will work.

## License

MIT
