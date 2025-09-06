from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email from provider")
    provider: str = Field(
        ..., description="Auth provider name (e.g., google, github, firebase)"
    )
    provider_id: str = Field(..., description="Unique ID from the auth provider")
    first_name: str | None = Field(
        None, max_length=50, description="First name from profile"
    )
    last_name: str | None = Field(
        None, max_length=50, description="Last name from profile"
    )
    avatar_url: str | None = Field(
        None, description="Profile picture URL from provider"
    )


class UserRead(BaseModel):
    id: int = Field(..., description="Unique identifier")
    email: EmailStr = Field(..., description="User email address")
    provider: str = Field(..., description="Auth provider name")
    provider_id: str = Field(..., description="Unique provider ID")
    first_name: str | None = Field(None, description="First name")
    last_name: str | None = Field(None, description="Last name")
    avatar_url: str | None = Field(None, description="Profile picture URL")
    created_at: str = Field(..., description="When the user was created")
    updated_at: str = Field(..., description="When the user was last updated")

    class Config:
        from_attributes = True
