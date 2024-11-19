from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schema import BookModel, BookUpdateModel
from src.books.book_data import books

book_router = APIRouter()


@book_router.get("/", response_model=List[BookModel])
def get_all_books() -> list:
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookModel):
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@book_router.get(
    "/book",
    response_model=BookModel,
    status_code=status.HTTP_200_OK
)
def get_book_by_id(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


@book_router.patch("/", response_model=BookUpdateModel)
def update_book_by_id(book_id: int, book_update: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book.update(book_update.model_dump())
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


@book_router.delete("/", status_code=status.HTTP_200_OK)
def delete_book_by_id(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
