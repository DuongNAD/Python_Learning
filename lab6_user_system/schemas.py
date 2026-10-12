import re
from pydantic import BaseModel, field_validator
from typing import Optional

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

class UserBase(BaseModel):
    name: str
    email: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Định dạng email không hợp lệ (ví dụ: user@example.com)")
        return v

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            if not re.match(EMAIL_REGEX, v):
                raise ValueError("Định dạng email không hợp lệ (ví dụ: user@example.com)")
        return v

class UserResponse(UserBase):
    id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str
