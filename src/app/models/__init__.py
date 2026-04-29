import uuid 

from sqlalchemy.orm import mapped_column
from sqlalchemy import UUID

from  typing_extensions import Annotated


id_uuid = Annotated[uuid.UUID,
                    mapped_column(primary_key=True, default=uuid.uuid4)]
