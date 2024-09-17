from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    authjwt_secret_key: str = "34237612c8feadb9c9dd530a7ba005631a84b50b3a09bab3ac500b7e48dbcf08"


class UserRegister(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]


class UserLogin(BaseModel):
    username_or_email: Optional[str]
    password: Optional[str]


class UserPasswordReset(BaseModel):
    password: Optional[str]
    confirm_password: Optional[str]
