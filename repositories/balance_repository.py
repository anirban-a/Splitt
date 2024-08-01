from typing import Optional

from bson import ObjectId
from pymongo.collection import Collection

from models import Balance


class BalanceRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def find(self, payer: str, payee: str, default: Balance = None) -> (Balance, str):
        entity = self.collection.find_one({'payer': payer, 'payee': payee})
        if (not entity) and default:
            return default, None
        return Balance.from_mongo(**entity), entity.get('_id')

    def save(self, balance: Balance, _id: ObjectId = None) -> Optional[Balance]:
        if _id:
            document_filter = {'_id': ObjectId(_id)}
            update = {"$set": {'amount': balance.amount}}
            self.collection.update_one(update=update, filter=document_filter)
            return None

        inserted_id = self.collection.insert_one(balance.model_dump()).inserted_id
        entity = self.collection.find_one({'_id': ObjectId(inserted_id)})
        return Balance.from_mongo(**entity)
