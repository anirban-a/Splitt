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
        txn_cursor = self.collection.find({'payer': payer})
        transactions = []
        while txn_cursor.alive:
            transactions.append(Transaction.from_mongo(**txn_cursor.next()))
        return transactions

    def get_all_by_payee(self, payee: str) -> List[Transaction]:
        txn_cursor = self.collection.find({'payee': payee})
        transactions = []
        while txn_cursor.alive:
            transactions.append(Transaction.from_mongo(**txn_cursor.next()))
        return transactions
        # return list(map(lambda txn: Transaction.from_mongo(**txn), l))

    def get_all_by_payee_and_group(self, payee: str, group_id: str) -> List[Transaction]:
        return list(map(Transaction.from_mongo, self.collection.find({'payee': payee, 'group_id': group_id})))
