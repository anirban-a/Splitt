from typing import List

from models import Transaction
from repositories.txn_repository import TransactionRepository
from .user_service import UserService


class TransactionService:
    def __init__(self, user_service: UserService, txn_repo: TransactionRepository):
        self.user_service = user_service
        self.txn_repo = txn_repo

    def create_transaction(self, txn: Transaction) -> Transaction:
        result = self.txn_repo.save(txn)
        return self.txn_repo.find_by_id(result.inserted_id)

    """A payer is someone who has already payed and is owed money to by other Payees. In other words, a payer is the 
    individual who has payed for the payee and now making a transaction log in the application making the now payee a 
    future potential payer."""

    def get_all_receivables(self, user_id: str) -> List[Transaction]:
        # get all transactions where money is owed to user_id
        return self.txn_repo.get_all_by_payer(user_id)

    def get_all_payable(self, user_id: str, group_id: str = None) -> List[Transaction]:
        return self.txn_repo.get_all_by_payee(user_id) if not group_id else self.txn_repo.get_all_by_payee_and_group(
            user_id, group_id)

    def compute_total_receivables(self, user_id: str) -> float:
        return sum(map(lambda txn: txn.amount, self.get_all_receivables(user_id)))

    def compute_total_payable(self, user_id: str) -> float:
        return sum(map(lambda txn: txn.amount, self.get_all_payable(user_id)))
