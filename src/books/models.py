from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid


class BookModel(SQLModel, table=True):
    __tablename__ = 'books'
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    publisher_date: date
    page_count: int
    language: str
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
        return f"<BOOK {self.title} by {self.author}>"