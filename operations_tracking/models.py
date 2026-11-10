"""Public input contract; no arbitrary database fields are accepted."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JobInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, allow_inf_nan=False)
    day: date
    time: str = Field(pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    title: str = Field(min_length=1, max_length=120)
    customer: str = Field(default="", max_length=100)
    site: str = Field(min_length=1, max_length=200)
    crew: str = Field(min_length=1, max_length=80)
    status: Literal["planned", "en_route", "on_site", "complete"] = "planned"
    travel_minutes: int = Field(default=0, ge=0, le=1440)
    site_minutes: int = Field(default=0, ge=0, le=1440)
    miles: float = Field(default=0, ge=0, le=2000)
    modules: int = Field(default=0, ge=0, le=5000)
    notes: str = Field(default="", max_length=2000)

    @field_validator("day")
    @classmethod
    def reasonable_year(cls, value):
        if not 2000 <= value.year <= 2100:
            raise ValueError("Use a date between 2000 and 2100.")
        return value


class JobUpdate(JobInput):
    version: int = Field(ge=1)


class Login(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(min_length=1, max_length=200)
