from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class LoggedUserResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

    class Config:
        orm_mode = True