class AlreadyExistsFileError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(f"File {filename} already exists.")

class NotFoundFileError(Exception):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(f"File {filename} dont exists.")