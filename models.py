from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    username: str
    groups: Optional[list[str]] = Field(None)

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def from_mongo(cls, **data):
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return cls(**data)


class Group(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
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
    id: Optional[str] = Field(None, alias='_id')
    payer: str
    payee: str
    amount: float = Field(0.0)
    group_id: Optional[str] = Field(None)

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def from_mongo(cls, **data):
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return cls(**data)


class Balance(BaseModel):
    _id: Optional[str]
    payer: str
    payee: str
    amount: float = Field(default=0.0)

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def from_mongo(cls, **data):
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        return cls(**data)
