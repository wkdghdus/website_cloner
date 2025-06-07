from pydantic import BaseModel, Field

class Reflection(BaseModel):
    similarity_result: bool = Field(description="True for roughly similar, False for not similar")
