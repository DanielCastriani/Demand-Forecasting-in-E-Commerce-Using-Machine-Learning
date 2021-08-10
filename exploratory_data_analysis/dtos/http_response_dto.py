from typing import Dict, List, TypedDict, Union


ResponseBodyDTO = Union[Dict, TypedDict, List[Union[Dict, TypedDict]], None]

class HTTPResponseDTO(TypedDict):
    body: ResponseBodyDTO
    success: bool
    message: str
    code: int
