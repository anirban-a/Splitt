from typing import List

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from models import Transaction


class TransactionRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def save(self, transaction: Transaction) -> InsertOneResult:
        return self.collection.insert_one(transaction.model_dump())

    def find_by_id(self, id: str) -> Transaction:
        entity = self.collection.find_one({'_id': ObjectId(id)})
        return Transaction.from_mongo(**entity)

    def get_all_by_payer(self, payer: str) -> List[Transaction]:
        return list(map(Transaction.from_mongo, self.collection.find({'payer': payer})))

    def get_all_by_payee(self, payee: str) -> List[Transaction]:
        return list(map(Transaction.from_mongo, self.collection.find({'payee': payee})))

    def get_all_by_payee_and_group(self, payee: str, group_id: str) -> List[Transaction]:
        return list(map(Transaction.from_mongo, self.collection.find({'payee': payee, 'group_id': group_id})))
