from pydantic import BaseModel, field_validator


class ItemCreate(BaseModel):
    name: str
    description: str = ""

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be blank")
        return v.strip()


class Item(BaseModel):
    id: int
    name: str
    description: str
