from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    username: str
    groups: list[str]

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def from_mongo(cls, **data):
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return cls(**data)


class Group(BaseModel):
    _id: str
    name: str
    members: list[str]

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def from_mongo(cls, **data):
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return cls(**data)


class Transaction(BaseModel):
    _id: str
    payer: str
    payee: str
    amount: float

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def from_mongo(cls, **data):
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return cls(**data)
