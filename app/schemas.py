"""Commented Imports"""
# from uuid import uuid4, UUID
from datetime import datetime
from pydantic import BaseModel

from typing import List, Dict, Union

from langchain_core.pydantic_v1 import Field


class ExperienceSchema(BaseModel):
    job_position: str = Field(description='Company name')
    responsibilities: List[str] = Field(description='List of responsibilities')


class Education(BaseModel):
    school_name: str
    certification: str = None
    course_study: str = None
    start_month: str = None
    start_year: int = None
    end_month: str = None
    end_year: int = None


class Responsibility(BaseModel):
    responsibility: str


class Experience(BaseModel):
    company_name: str
    position: str
    start_month: str = None
    start_year: int = None
    end_month: str = None
    end_year: int = None
    experience_responsibilities: List[Responsibility] = None


class Skill(BaseModel):
    name: str
    skill_level: str
    year_of_experience: int


class Certification(BaseModel):
    name: str
    issued_date: datetime = None
    expiry_date: datetime = None
    url: str = None


class ProfileBase(BaseModel):
    full_name: str
    email: str
    phone_number: str
    gender: str
    country: str = None
    state: str = None
    job_title: str
    portfolio_website: str = None
    github_url: str = None
    linkedin_url: str = None
    dribble_url: str = None


class Profile(ProfileBase):
    profile_educations: List[Education] = []
    profile_experiences: List[Experience] = []
    profile_certifications: List[Certification] = []
    profile_skills: List[Skill] = []

    class Config:
        from_attributes = True

