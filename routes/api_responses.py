from pydantic import BaseModel


class BalanceResponseItem(BaseModel):
    user_id: str
    balance: float

    class Config:
        schema_extra = {
            'example': {
                'user_id': '66aad02f0359ae9fc1dde561',
                'balance': 10.0
            }
        }


class BalanceListResponseItem(BaseModel):
    balances: list[BalanceResponseItem]

    class Config:
        schema_extra = {
            'example': {
                'balances': [{
                    'user_id': '66aad02f0359ae9fc1dde561',
                    'balance': 10.0
                }]
            }
        }
