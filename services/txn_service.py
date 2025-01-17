from typing import List

from models import Transaction, Balance
from repositories.balance_repository import BalanceRepository
from repositories.txn_repository import TransactionRepository
from .user_service import UserService


class TransactionService:
    def __init__(self, user_service: UserService, txn_repo: TransactionRepository, balance_repo: BalanceRepository):
        self.user_service = user_service
        self.txn_repo = txn_repo
        self.balance_repo = balance_repo

    def create_transaction(self, txn: Transaction) -> Transaction:
        # balance_id, rev_balance_id = TransactionService.__create_balance_id(txn.payer, txn.payee)

        balance, balance_id = self.balance_repo.find(payer=txn.payer, payee=txn.payee,
                                                     default=Balance(
                                                         **{'payer': txn.payer, 'payee': txn.payee, 'amount': 0.0}))
        rev_balance, rev_balance_id = self.balance_repo.find(payee=txn.payer, payer=txn.payee,
                                                             default=Balance(**{'payee': txn.payer, 'payer': txn.payee,
                                                                                'amount': 0.0}))
        balance.amount += txn.amount
        rev_balance.amount -= txn.amount

        self.balance_repo.save(balance, balance_id)
        self.balance_repo.save(rev_balance, rev_balance_id)

        result = self.txn_repo.save(txn)
        return self.txn_repo.find_by_id(result.inserted_id)

    """A payer is someone who has already payed and is owed money to by other Payees. In other words, a payer is the 
    individual who has payed for the payee and now making a transaction log in the application making the now payee a 
    future potential payer."""

    def get_all_receivables(self, user_id: str) -> List[Balance]:
        # get all transactions where money is owed to user_id
        # return self.txn_repo.get_all_by_payer(user_id)
        return self.balance_repo.find_all_by_payer_receivable(user_id)

    def get_all_payable(self, user_id: str, group_id: str = None) -> List[Balance]:
        return self.balance_repo.find_all_by_payer_payable(user_id, group_id)

    def compute_total_receivables(self, user_id: str) -> float:
        ''' Calculate the total sum of money owed to the user by others. '''
        # total_balance = sum(map(lambda txn: txn.amount, self.get_all_receivables(user_id))) - sum(
        #     map(lambda txn: txn.amount, self.get_all_payable(user_id)))
        total_balance = sum(map(lambda balance: balance.amount, self.get_all_receivables(user_id)))
        return max(0, total_balance)

    def compute_total_payable(self, user_id: str) -> float:
        ''' Calculate the total sum of money the user owes others. '''
        # total_balance = sum(map(lambda txn: txn.amount, self.get_all_payable(user_id))) - sum(
        #     map(lambda txn: txn.amount, self.get_all_receivables(user_id)))
        total_balance = sum(map(lambda balance: balance.amount, self.get_all_payable(user_id)))
        return max(0, total_balance)
