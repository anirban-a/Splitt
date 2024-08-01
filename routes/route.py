from __future__ import annotations

from functools import lru_cache

from fastapi import APIRouter, Depends
from pymongo import MongoClient, database
from pymongo.collection import Collection

from config.config import BaseConfig
from models import User, Transaction
from repositories.balance_repository import BalanceRepository
from repositories.txn_repository import TransactionRepository
from repositories.user_repository import UserRepository
from services.txn_service import TransactionService
from services.user_service import UserService
from .api_responses import BalanceResponseItem, BalanceListResponseItem

router = APIRouter()

user_router = APIRouter(prefix='/user')
txn_router = APIRouter(prefix='/transaction')


@lru_cache
def get_settings():
    return BaseConfig()


def get_db(base_config: BaseConfig = Depends(get_settings)) -> database.Database:
    client = MongoClient(base_config.MONGO_URL)
    return client.get_database(base_config.DATABASE_NAME)


def get_user_collection(db: database.Database = Depends(get_db)) -> Collection:
    return db.get_collection('user')


def get_txn_collection(db: database.Database = Depends(get_db)) -> Collection:
    return db.get_collection('transaction')


def get_balance_collection(db: database.Database = Depends(get_db)) -> Collection:
    return db.get_collection('balance')


def get_txn_repository(txn_collection: Collection = Depends(get_txn_collection)):
    return TransactionRepository(txn_collection)


def get_balance_repository(balance_collection: Collection = Depends(get_balance_collection)):
    return BalanceRepository(balance_collection)


def get_user_repository(user_collection: Collection = Depends(get_user_collection)):
    return UserRepository(user_collection)


def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)


def get_txn_service(user_service: UserService = Depends(get_user_service),
                    txn_repository: TransactionRepository = Depends(get_txn_repository),
                    balance_repository: BalanceRepository = Depends(get_balance_repository)):
    return TransactionService(user_service, txn_repository, balance_repository)


@user_router.post("/")
async def create_user(user: User, user_service: UserService = Depends(get_user_service)):
    _user = user_service.create_user(user)
    return _user


@txn_router.post("/")
async def create_txn(txn: Transaction, txn_service: TransactionService = Depends(get_txn_service)):
    _txn = txn_service.create_transaction(txn)
    return _txn


@txn_router.get("/out-bound-balance/{user_id}",
                summary='Get the total sum of money the user with `user_id` owes to other users',
                response_model=BalanceResponseItem)
async def get_out_bound_balance(user_id: str, txn_service: TransactionService = Depends(get_txn_service)):
    balance = txn_service.compute_total_payable(user_id)
    return BalanceResponseItem(**{'user_id': user_id, 'balance': balance})


@txn_router.get("/in-bound-balance/{user_id}",
                summary='Get the total sum of money other users owe to the user with `user_id`',
                response_model=BalanceResponseItem)
async def get_in_bound_balance(user_id: str, txn_service: TransactionService = Depends(get_txn_service)):
    balance = txn_service.compute_total_receivables(user_id)
    return BalanceResponseItem(**{'user_id': user_id, 'balance': balance})


@txn_router.get("/all-out-bound-balance/{user_id}")
async def get_all_out_bound_balance(user_id: str, group_id: str | None = None,
                                    txn_service: TransactionService = Depends(get_txn_service),
                                    response_model=BalanceListResponseItem):
    balances = txn_service.get_all_payable(user_id, group_id)
    return BalanceListResponseItem(**{'balances': balances})

    # return BalanceResponseItem(**{'user_id': user_id, 'balance': balance})


router.include_router(user_router)
router.include_router(txn_router)
# Get total sum of money I owe to people -> done
# Get total sum of money owed to me -> done
# Get total sum of money I owe to each individual -> done
# Get total sum of money I owe to each individual filtered by group -> done
# Create a group
# Delete a group
# Assign a user to a group
# Remove a user from a group
