from pydantic import BaseModel


class BookModel(BaseModel):
    id: int
    title: str
    author: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
