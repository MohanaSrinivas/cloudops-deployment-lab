from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

Status = Literal["saved", "applied", "interview", "offer", "rejected"]

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserRead(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=160)
    role: str = Field(min_length=1, max_length=160)
    status: Status = "saved"
    job_url: HttpUrl | None = None
    notes: str = Field(default="", max_length=10000)

class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=160)
    role: str | None = Field(default=None, min_length=1, max_length=160)
    status: Status | None = None
    job_url: HttpUrl | None = None
    notes: str | None = Field(default=None, max_length=10000)

class ApplicationRead(BaseModel):
    id: int
    company: str
    role: str
    status: Status
    job_url: str | None
    notes: str
    applied_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Statistics(BaseModel):
    total: int
    by_status: dict[str, int]
    response_rate: float
