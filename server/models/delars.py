from typing import Optional

from pydantic import BaseModel, Field


# Delar Schema
class DelarSchema(BaseModel):
    name: str = Field(...)
    location: str = Field(...)
    state: str = Field(...)
    phone: str = Field(...)
# Update Delar 
class UpdateDelarSchema(BaseModel):
    name: Optional[str]
    location: Optional[str]
    state: Optional[str]
    phone: Optional[str]    
# res
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }
# Error
def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }