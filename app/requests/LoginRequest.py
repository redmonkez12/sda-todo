from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(description="The field username is mandatory")
    password: str = Field(description="The field password is mandatory")

    class Config:
        schema_extra = {
            "example": {
                "username": "funkymoney123",
                "password": "123456",
            }
        }

        description = "Login credentials"
        fields = {
            "username": {
                "description": "The user's username"
            },
            "password": {
                "description": "The user's password"
            }
        }

