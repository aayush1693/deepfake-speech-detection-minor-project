"""Tests for the application factory.

Importing the app and these tests must not require TensorFlow, librosa,
matplotlib, or requests; CI only installs Flask, flask-cors, and python-dotenv.
"""

import os

import app as app_module
from app import create_app


class OverrideConfig:
    MODEL_PATH = 'custom/weights.h5'
    TESTING = True


def test_module_level_app_is_created():
    assert app_module.app is not None
    assert app_module.app.test_client() is not None


def test_health_reports_missing_model(tmp_path, monkeypatch):
    missing_model = tmp_path / 'missing-weights.h5'
    monkeypatch.setattr(app_module.config, 'MODEL_PATH', str(missing_model))

    application = create_app()

    assert not os.path.exists(missing_model)
    assert application.config['MODEL_PATH'] == str(missing_model)

    response = application.test_client().get('/api/health')

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['model_present'] is False
    assert payload['status'] == 'UP'


def test_create_app_applies_dict_overrides_after_defaults(tmp_path):
    override_path = str(tmp_path / 'override.h5')
    application = create_app({
        'MODEL_PATH': override_path,
        'MAX_UPLOAD_BYTES': 1024,
    })

    assert application.config['MODEL_PATH'] == override_path
    assert application.config['MAX_CONTENT_LENGTH'] == 1024
    # Defaults that were not overridden are still present.
    assert application.config['UPLOAD_FOLDER'] == app_module.config.UPLOAD_FOLDER


def test_create_app_accepts_config_object():
    application = create_app(OverrideConfig)

    assert application.config['MODEL_PATH'] == 'custom/weights.h5'
    assert application.config['TESTING'] is True
    assert application.config['UPLOAD_FOLDER'] == app_module.config.UPLOAD_FOLDER


def test_health_uses_app_config_not_module_config(tmp_path):
    missing_model = tmp_path / 'absent.h5'
    application = create_app({'MODEL_PATH': str(missing_model)})

    payload = application.test_client().get('/api/health').get_json()

    assert payload['model_present'] is False
