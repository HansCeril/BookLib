from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schema import CompleteBookModel, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService


book_router = APIRouter()
books = BookService()


@book_router.get("/", response_model=List[CompleteBookModel])
async def get_all_books(session: AsyncSession = Depends(get_session)) -> list:
    all_book = await books.get_all_books(session)
    return all_book


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CompleteBookModel
)
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session)
):
    new_book = await books.create_book(book_data, session)
    return new_book


@book_router.get(
    "/book",
    response_model=CompleteBookModel,
    status_code=status.HTTP_200_OK
)
async def get_book_by_id(
    book_id: str,
    session: AsyncSession = Depends(get_session)
) -> dict:
    book = await books.get_book(book_id, session)
    if book is not None:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


@book_router.patch("/", response_model=CompleteBookModel)
async def update_book_by_id(
    book_id: str,
    book_update: BookUpdateModel,
    session: AsyncSession = Depends(get_session)
) -> dict:
    book = await books.update_book(book_id, book_update, session)
    if book is not None:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


@book_router.delete("/", status_code=status.HTTP_200_OK, response_model=CompleteBookModel)
async def delete_book_by_id(
    book_id: str,
    session: AsyncSession = Depends(get_session)
) -> dict:
    book = await books.delete_book(book_id, session)
    if book is not None:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
