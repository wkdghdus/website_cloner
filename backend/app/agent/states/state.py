from typing import Optional
from pydantic import Field, BaseModel


class State(BaseModel):
    cloned_website: Optional[str] = Field(default=None)
    given_url: Optional[str] = Field(default=None)
    raw_html: Optional[str] = Field(default=None)
    stylesheets: Optional[dict] = Field(default=None)
    images: Optional[list[str]] = Field(default=None)
    screen_shot: Optional[str] = Field(default=None)
    meta: Optional[list[dict]] = Field(default=None)
    fonts: Optional[str] = Field(default=None)
    validation: Optional[bool] = Field(default=None)