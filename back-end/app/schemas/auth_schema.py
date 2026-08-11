from pydantic import BaseModel


class Login(BaseModel):
    email_id: str
    password: str


class Signup(BaseModel):
    first_name: str
    last_name: str
    email_id: str
    password: str


class OtpVerify(BaseModel):
    email_id: str


class Validation(BaseModel):
    email_id: str
    otp: str
