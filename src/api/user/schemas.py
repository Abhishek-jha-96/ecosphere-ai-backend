from pydantic import BaseModel, EmailStr, Field

from api.user.constants import AuthProvider


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email from provider")
    provider: AuthProvider = Field(..., description="Auth provider name")
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
    provider: AuthProvider = Field(..., description="Auth provider name")
    provider_id: str = Field(..., description="Unique provider ID")
    first_name: str | None = Field(None, description="First name")
    last_name: str | None = Field(None, description="Last name")
    avatar_url: str | None = Field(None, description="Profile picture URL")
    created_at: str = Field(
        ...,
    )
    updated_at: str = Field(
        ...,
    )

    class Config:
        from_attributes = True
