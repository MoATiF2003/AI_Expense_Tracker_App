from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str

    type: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int

    name: str

    type: Optional[str]

    class Config:
        from_attributes = True

class CategoryBasicResponse(BaseModel):
    id: int

    name: str

    class Config:
        from_attributes = True