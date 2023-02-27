from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, constr

# User Schema
class UserSchema(BaseModel):
    firstname: str = Field(...)
    middlename: str = Field(...)
    lastname: str = Field(...)
    username: str = Field(...)
    phone: str = Field(...,min_length=9,)
    email: EmailStr = Field(...)
    location: str = Field(...)
    vip: int = Field(...)
    phoneVerfication: bool = False
    emailVerfication: bool = False
    balance: int = 0
    pendingBalance : int = 0
    sms_code: str = Field(...)
    email_code: str = Field(...)
    created_at: datetime | None
    class Config:
        orm_mode = True
# password
class CreateUserSchema(UserSchema):
    password: constr(min_length=8)
    password_confirm: str
# Login
class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
# Response
class UserResponseSchema(UserSchema):
    id: str
    pass
# User Response
class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema
# Update User Schema   
class UpdateUserModel(BaseModel):
    firstname: Optional[str]
    middlename: Optional[str]
    lastname: Optional[str]
    username: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    location: Optional[str]
    vip: Optional[int]
    phoneVerfication: Optional[bool]
    emailVerfication: Optional[bool]
    balance: Optional[int]
    pendingBalance: Optional[int]
    password: Optional[str]

class ResponsModels():
    # Response
    def ResponseModel(data, message):
        return {
            "data": [data],
            "code": 200,
            "message": message
        }
    # Error Response
    def ErrorResponseModel(error, code, message):
        return {
            "error": error,
            "code": code,
            "message": message
        }
    