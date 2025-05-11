from sqlalchemy import (
    BOOLEAN,
    BigInteger,
    Column,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Users(Base):

    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=False)
    ban = Column(BOOLEAN, default=False)

    def __str__(self):
        return f"User @{self.username}"
