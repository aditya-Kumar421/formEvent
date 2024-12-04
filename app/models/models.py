from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List

app = FastAPI()

class Participant(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    student_no: str = Field(
        ...,
        pattern=r"^(23|24)[A-Za-z0-9]*$",  # Matches student numbers starting with 23 or 24
        min_length=5,
        max_length=11
    )
    mobile: str = Field(..., pattern="^[0-9]{10}$")
    gender: str = Field(..., min_length=3, max_length=8) 
    branch: str = Field(..., min_length=2, max_length=50)
    unstop: str = Field(..., min_length=1, max_length=50)
    residence: str = Field(..., min_length=2, max_length=100)

    @field_validator("email")
    def validate_email(cls, value, info):
        student_no = info.data.get("student_no")
        if not value.endswith("@akgec.ac.in"):
            raise ValueError("Email must end with '@akgec.ac.in'.")
        if student_no and student_no not in value:
            raise ValueError("Email must contain the student number.")
        return value
    
    @field_validator("student_no")
    def validate_student_no(cls, value):
        if not value.startswith(("23", "24")):
            raise ValueError("Student number must start with 23 or 24.")
        return value


class Registration(BaseModel):
    team_name: str = Field(..., min_length=2, max_length=100)
    domain_name: str = Field(..., min_length=2, max_length=100)
    participants: List[Participant] = Field(..., min_items=2, max_items=2)
    recaptcha_response: str = Field(..., min_length=10, exclude=True)

    @field_validator("participants")
    def validate_participants(cls, value):
        if len(value) != 2:
            raise ValueError("Exactly two participants are required.")
        return value

