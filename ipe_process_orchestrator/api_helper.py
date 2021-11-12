from typing import Optional
from requests import Response

def response_none_check(response: Optional[Response], message: str) -> None:
    if response is None:
        raise Exception(message)
