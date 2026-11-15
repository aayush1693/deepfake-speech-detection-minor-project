"""Tests for the JSON error envelope returned by the ML service."""

import io

import pytest

from app import create_app


def assert_error(response, status, code):
    assert response.status_code == status
    assert response.is_json

    payload = response.get_json()
    assert payload['code'] == code
    assert payload['error']
    return payload


@pytest.fixture
def client():
    return create_app({'TESTING': True}).test_client()


def test_unknown_route_returns_json_404(client):
    payload = assert_error(client.get('/api/unknown'), 404, 'NOT_FOUND')

    assert 'not found' in payload['error'].lower()


def test_wrong_method_returns_json_405(client):
    assert_error(client.get('/api/predict'), 405, 'METHOD_NOT_ALLOWED')


def test_oversized_payload_returns_json_413(monkeypatch):
    application = create_app({'TESTING': True})
    monkeypatch.setitem(application.config, 'MAX_CONTENT_LENGTH', 1024)

    response = application.test_client().post(
        '/api/predict',
        data={'file': (io.BytesIO(b'x' * 4096), 'clip.wav')},
    )

    payload = assert_error(response, 413, 'PAYLOAD_TOO_LARGE')
    assert 'MAX_UPLOAD_BYTES' in payload['error']


def test_unsupported_media_type_returns_json_415(client):
    response = client.post('/api/predict', json={'file': 'clip.wav'})

    assert_error(response, 415, 'UNSUPPORTED_MEDIA_TYPE')


def test_missing_file_keeps_explicit_400_message(client):
    response = client.post(
        '/api/predict',
        data={'other': (io.BytesIO(b'not audio'), 'notes.txt')},
    )

    payload = assert_error(response, 400, 'BAD_REQUEST')
    assert payload['error'] == 'No file provided'


def test_unsupported_extension_keeps_explicit_400_message(client):
    response = client.post(
        '/api/predict',
        data={'file': (io.BytesIO(b'not audio'), 'clip.txt')},
    )

    payload = assert_error(response, 400, 'BAD_REQUEST')
    assert payload['error'] == 'Unsupported audio format'
    assert payload['allowed'] == ['flac', 'm4a', 'mp3', 'ogg', 'wav', 'webm']


def test_internal_error_returns_json_without_details():
    application = create_app({'TESTING': False, 'PROPAGATE_EXCEPTIONS': False})

    @application.route('/api/boom')
    def boom():
        raise RuntimeError('secret path /srv/private/weights.h5')

    response = application.test_client().get('/api/boom')

    payload = assert_error(response, 500, 'INTERNAL_SERVER_ERROR')
    assert payload['error'] == 'Internal server error'

    body = response.get_data(as_text=True)
    assert 'secret path' not in body
    assert '/srv/private' not in body
    assert 'Traceback' not in body
