import uuid

from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

id_uuid = Annotated[uuid.UUID, mapped_column(primary_key=True, default=uuid.uuid4)]

from .user_account import User
from .user_account import Account as AccountInfo
from .transaction import Transaction
from .account import Account
