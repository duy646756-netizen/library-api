from pydantic import BaseModel, Field

class BookBase(BaseModel):
    isbn: str = Field(pattern=r"^\d{13}$", examples=["9786040000011"])
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1900, le=2100)
    quantity: int = Field(default=1, ge=0)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1900, le=2100)
    quantity: int | None = Field(default=None, ge=0)

class BookOut(BookBase):
    id: int