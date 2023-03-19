
from pydantic import BaseModel, Field


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(description="The field old_password is mandatory")
    new_password: str = Field(description="The field new_password is mandatory")
