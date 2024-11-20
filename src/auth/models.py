from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class UserModel(SQLModel, table=True):
    __tablename__ = 'users'
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    first_name: str
    last_name: str
    email: str
    password_hash: str = Field(
        exclude=True
    )
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now()
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now()
        )
    )

    def __repr__(self):
        return f"<USER {self.username}>"
