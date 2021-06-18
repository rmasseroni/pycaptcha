import flask
from flask import jsonify
from flask import request
from services.CaptchaService import CaptchaService
from models.CaptchaRequest import CaptchaRequest
from logger_config import logger


def configure_routes(app, captcha_service):
    @app.route('/', methods=['GET'])
    def generate_form():
        id_form, captcha_b64 = captcha_service.new_form()
        return jsonify({
            "uuid": id_form,
            "image": captcha_b64
        })

    @app.route('/', methods=['POST'])
    def subscribe():
        try:
            subscribe_request = CaptchaRequest(
                request.json['id_form'],
                request.json['captcha'],
            )
        except Exception as e:
            logger.error(e)
            return jsonify({"message": str(e)}), 400

        valid_captcha = captcha_service.verify(subscribe_request)
        return (jsonify({"message": "Valid captcha"}), 200) if valid_captcha else (jsonify({"message": "Invalid captcha"}), 400)


if __name__ == '__main__':
    flask_app = flask.Flask(__name__)
    configure_routes(flask_app, CaptchaService())
    flask_app.run(host='0.0.0.0', port=8080)
