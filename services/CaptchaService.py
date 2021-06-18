import base64
import sqlite3
import uuid
import random
import string
from logger_config import logger

from captcha.image import ImageCaptcha
from models.CaptchaRequest import CaptchaRequest
from repositories.CaptchaRepository import CaptchaRepository


class CaptchaService:
    def __init__(self):
        try:
            logger.debug('Connecting to SQLite database...')
            self.database_connection = sqlite3.connect('test.db', check_same_thread=False)
            logger.debug('Connected to SQLite database')
            self.captcha_repository = CaptchaRepository(self.database_connection)
            self.captcha_repository.create_table()
        except Exception as e:
            logger.error(e)
            raise e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.database_connection.close()

    def verify(self, request: CaptchaRequest):
        """Verify captcha code for the given from.

        :param request: valid CaptchaRequest.
        """
        if not request:
            raise Exception("Invalid request")

        valid_captcha = self.captcha_repository.check(request.id_form, request.captcha)
        self.captcha_repository.update_form(request.id_form)
        return True if valid_captcha else False

    def new_form(self):
        """Generate a new form with its relative captcha
        """
        id_form = str(uuid.uuid4())
        captcha = self.random_alphanumeric_string(7)
        self.captcha_repository.create_form(id_form, captcha)
        logger.debug("Created new form with id {} and captcha {}".format(id_form, captcha))
        image = ImageCaptcha(width=280, height=90)
        return id_form, base64.b64encode(image.generate(captcha).getvalue()).decode('utf-8')

    @staticmethod
    def random_alphanumeric_string(length):
        """
        Generate a random alphanumeric string
        :return: Random alphanumeric string (uppercase letters + digits)
        """
        generated_string = ''
        for i in range(length):
            generated_string += random.choice(string.ascii_uppercase + string.digits)
        return generated_string
