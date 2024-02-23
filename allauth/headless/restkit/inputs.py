from django.forms import CharField, EmailField, Form, ValidationError

from allauth.headless.restkit.response import ErrorResponse


__all__ = ["CharField", "ValidationError", "EmailField"]


class Input(Form):
    @property
    def error_dict(self):
        ret = {}
        ret.update(self.errors)
        return ret

    def respond_error(self):
        return ErrorResponse(self.error_dict)
