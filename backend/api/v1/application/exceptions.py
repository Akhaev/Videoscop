class UnAuthorizedError(Exception):
    pass

class ValidationError(Exception):
    def __init__(self, errors):
        self.errors_list = errors

    def __str__(self):
        return f"Validation errors: {self.errors_list}"

    def errors(self):
        return self.errors_list

    @classmethod
    def add_error(cls, field: str, msg: str):
        return {"loc": (field,), "msg": msg, "type": "value_error"}