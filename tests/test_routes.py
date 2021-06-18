from uuid import UUID
from flask import Flask
from app import configure_routes
from services.CaptchaService import CaptchaService


def test_should_generate_uuid_and_base64_image():
    app = Flask(__name__)
    configure_routes(app, CaptchaService())
    client = app.test_client()
    url = '/'

    response = client.get(url)
    response_json = response.get_json()
    assert response.status_code == 200
    assert validate_uuid4(response_json['uuid'])
    assert len(response_json['image']) > 10000


def test_should_return_bad_request_because_nonexistent_form():
    app = Flask(__name__)
    configure_routes(app, CaptchaService())
    client = app.test_client()
    url = '/'

    response = client.post(url, json={
        "id_form": "06ab8279-ffbd-49ef-96e8-025d593dffe8",
        "captcha": "V6AKX51"
    })
    response_json = response.get_json()
    assert response_json['message'] == 'Invalid captcha'
    assert response.status_code == 400


def test_should_generate_and_validate_captcha(mocker):
    mocker.patch('services.CaptchaService.CaptchaService.random_alphanumeric_string', return_value='V6AKX51')

    app = Flask(__name__)
    configure_routes(app, CaptchaService())
    client = app.test_client()
    url = '/'

    get_response = client.get(url)
    assert get_response.status_code == 200

    post_response = client.post(url, json={
        "id_form": get_response.get_json()['uuid'],
        "captcha": "V6AKX51"
    })
    response_json = post_response.get_json()
    assert response_json['message'] == 'Valid captcha'
    assert post_response.status_code == 200


def test_should_generate_and_not_validate_the_second_time(mocker):
    mocker.patch('services.CaptchaService.CaptchaService.random_alphanumeric_string', return_value='MOCKED_CAPTCHA')

    app = Flask(__name__)
    configure_routes(app, CaptchaService())
    client = app.test_client()
    url = '/'

    get_response = client.get(url)
    assert get_response.status_code == 200

    post_response = client.post(url, json={
        "id_form": get_response.get_json()['uuid'],
        "captcha": "MOCKED_CAPTCHA"
    })
    response_json = post_response.get_json()
    assert response_json['message'] == 'Valid captcha'
    assert post_response.status_code == 200

    post_response = client.post(url, json={
        "id_form": get_response.get_json()['uuid'],
        "captcha": "MOCKED_CAPTCHA"
    })
    response_json = post_response.get_json()
    assert response_json['message'] == 'Invalid captcha'
    assert post_response.status_code == 400


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True
