from pydantic import BaseModel


class User(BaseModel):
    username: str
    groups: list[str]


class Group(BaseModel):
    name: str
    members: list[str]


class Transaction(BaseModel):
    id: str
    payer: str
    payee: str
