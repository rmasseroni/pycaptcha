from dataclasses import dataclass


@dataclass
class CaptchaRequest(object):
    id_form: str
    captcha: str

    def __post_init__(self):
        if not self.id_form:
            raise ValueError("Invalid form ID")
        if not self.captcha:
            raise ValueError("Invalid captcha")
