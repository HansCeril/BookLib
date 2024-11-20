from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schema import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from src.books.models import BookModel
from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uuid: str, session: AsyncSession):
        statement = select(BookModel).where(BookModel.uid == book_uuid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(
        self, book_data: BookCreateModel, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()
        new_book = BookModel(**book_data_dict)
        new_book.publisher_date = datetime.strptime(
            book_data_dict["publisher_date"], "%Y-%m-%d"
        )
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, book_uuid: str, book_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uuid, session)

        if book_to_update is not None:
            book_data_dict = book_data.model_dump()
            for key, value in book_data_dict.items():
                setattr(book_to_update, key, value)
            await session.commit()
            return book_to_update
        else:
            return None

    async def delete_book(self, book_uuid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uuid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return book_to_delete
        else:
            return None
