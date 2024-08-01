from typing import List

from models import Transaction, Balance
from repositories.balance_repository import BalanceRepository
from repositories.txn_repository import TransactionRepository
from .user_service import UserService


class TransactionService:
    # @staticmethod
    # def __create_balance_id(payer_id: str, payee_id: str) -> List[str]:
    #     id_1 = b'{payer_id}{payee_id}'
    #     id_2 = b'{payee_id}{payer_id}'
    #     hash_1 = blake2b(id_1, digest_size=12, key=b'helloworld')
    #     hash_2 = blake2b(id_2, digest_size=12, key=b'helloworld')
    #     return [hash_1.hexdigest(), hash_2.hexdigest()]

    def __init__(self, user_service: UserService, txn_repo: TransactionRepository, balance_repo: BalanceRepository):
        self.user_service = user_service
        self.txn_repo = txn_repo
        self.balance_repo = balance_repo

    def create_transaction(self, txn: Transaction) -> Transaction:
        # balance_id, rev_balance_id = TransactionService.__create_balance_id(txn.payer, txn.payee)

        balance = self.balance_repo.find(payer=txn.payer, payee=txn.payee,
                                         default=Balance(**{'payer': txn.payer, 'payee': txn.payee, 'amount': 0.0}))
        rev_balance = self.balance_repo.find(payee=txn.payer, payer=txn.payee,
                                             default=Balance(**{'payee': txn.payer, 'payer': txn.payee, 'amount': 0.0}))
        balance.amount += txn.amount
        rev_balance.amount -= txn.amount

        self.balance_repo.save(balance)
        self.balance_repo.save(rev_balance)

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
        ''' Calculate the total sum of money owed to the user by others. '''
        total_balance = sum(map(lambda txn: txn.amount, self.get_all_receivables(user_id))) - sum(
            map(lambda txn: txn.amount, self.get_all_payable(user_id)))
        return max(0, total_balance)

    def compute_total_payable(self, user_id: str) -> float:
        ''' Calculate the total sum of money the user owes others. '''
        total_balance = sum(map(lambda txn: txn.amount, self.get_all_payable(user_id))) - sum(
            map(lambda txn: txn.amount, self.get_all_receivables(user_id)))
        return max(0, total_balance)
