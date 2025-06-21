from pydantic import BaseModel
from typing import Optional, Union

class APIResponse(BaseModel):
    """
    Base model for API responses.
    """
    success: bool
    message: str 
    data: Optional[Union[dict, list]] = None

def ApiResponseHelper(success: bool, message: str, data: Union[dict, list, str, None] = None):
    return {"success": success, "message": message, "data": data}