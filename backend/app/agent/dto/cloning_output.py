from pydantic import BaseModel, Field

class Clone(BaseModel):
    html_output: str = Field(description="a complete HTML document as a string")
