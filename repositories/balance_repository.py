from typing import Optional, List

from bson import ObjectId
from pymongo.collection import Collection

from models import Balance


class BalanceRepository:

    @staticmethod
    def __cursor_to_list(balance_cursor):
        balances = []
        while balance_cursor.alive:
            balance = Balance.from_mongo(**balance_cursor.next())
            balances.append(balance)
        return balances

    def __init__(self, collection: Collection):
        self.collection = collection

    def find(self, payer: str, payee: str, default: Balance = None) -> (Balance, str):
        entity = self.collection.find_one({'payer': payer, 'payee': payee})
        if (not entity) and default:
            return default, None
        return Balance.from_mongo(**entity), entity.get('_id')

    def find_all_by_payer(self, payer: str) -> List[Balance]:
        balance_cursor = self.collection.find({'payer': payer})
        return BalanceRepository.__cursor_to_list(balance_cursor)

    def find_all_by_payer_receivable(self, payer: str) -> List[Balance]:
        balance_cursor = self.collection.find({'payer': payer}, filter={'amount': {'$lt': 0}})
        return BalanceRepository.__cursor_to_list(balance_cursor)

    def find_all_by_payer_payable(self, payer: str, group_id: str = None) -> List[Balance]:
        find_by = {'payer': payer}
        if group_id:
            find_by['group_id'] = group_id
        balance_cursor = self.collection.find(find_by, filter={'amount': {'$gt': 0}})
        return BalanceRepository.__cursor_to_list(balance_cursor)

    def save(self, balance: Balance, _id: ObjectId = None) -> Optional[Balance]:
        if _id:
            document_filter = {'_id': ObjectId(_id)}
            update = {"$set": {'amount': balance.amount}}
            self.collection.update_one(update=update, filter=document_filter)
            return None

        inserted_id = self.collection.insert_one(balance.model_dump()).inserted_id
        entity = self.collection.find_one({'_id': ObjectId(inserted_id)})
        return Balance.from_mongo(**entity)
