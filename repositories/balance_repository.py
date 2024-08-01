from typing import Optional

from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from models import Balance


class BalanceRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def find(self, payer: str, payee: str, default: Balance = None) -> Optional[Balance]:
        entity = self.collection.find_one({'payer': payer, 'payee': payee})
        if (not entity) and default:
            return default
        return Balance.from_mongo(**entity)

    def save(self, balance: Balance) -> InsertOneResult:
        return self.collection.insert_one(balance.model_dump())
