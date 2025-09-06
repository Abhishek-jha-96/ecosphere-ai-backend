from pydantic import BaseModel, EmailStr, Field


class MyModelCreate(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=8, max_length=128, description="User password"
    )
    first_name: str = Field(..., min_length=1, max_length=50, description="First name")
    last_name: str | None = Field(
        None, min_length=1, max_length=50, description="Last name (optional)"
    )


class MyModelRead(BaseModel):
    id: int = Field(..., description="Unique identifier")
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., description="First name")
    last_name: str | None = Field(None, description="Last name (optional)")
    created_at: str = Field(..., description="Timestamp when record was created")
    updated_at: str = Field(..., description="Timestamp when record was last updated")

    class Config:
        from_attributes = True  # enables ORM mode for SQLAlchemy
