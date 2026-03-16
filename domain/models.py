from pydantic import BaseModel
from datetime import datetime

class ErrorLog(BaseModel):
    timestamp: datetime
    exception_type: str
    message: str
    cloud_RoleInstance:str
    cloud_RoleName: str


class ErrorCategory(BaseModel):
    category: str
    count: int