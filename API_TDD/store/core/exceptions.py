class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message
    
    def __str__(self) -> str:
        return self.message


class NotFoundException(BaseException):
    message = "Not Found"
