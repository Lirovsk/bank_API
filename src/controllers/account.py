from ..app import db
from ..app.models.user_account import Account
from . import user

from flask import Blueprint, request

app = Blueprint("account", __name__, url_prefix="/accounts")

# function responsible to create a new account, it will receive a json with the name and email of the account, if the email already exists it will raise an error
def create_account(data: dict):
    pass


def serch_accounts():
    pass


def search_account(account_email: str):
    pass


