from application import interfaces

class FIleStorage(interfaces.GetFileUploadLink):
    def __init__(self) -> None:
        pass
    
    async def get_upload_link(self, filename: str) -> str:
        return f"https://storage.googleapis.com/{filename}"