from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schema import UserCreateModel
from sqlmodel import select, desc
from src.auth.models import UserModel
from datetime import datetime
from src.auth.utils import generate_password_hash, verify_password


class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        """
        Retrieve a user from the database by their email address.

        Args:
            email (str): The email address of the user to retrieve.
            session (AsyncSession): The asynchronous database session for
            executing queries.

        Returns:
            UserModel | None: The user object if found; otherwise, None.
        """
        statement = select(UserModel).where(UserModel.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user if user is not None else None

    async def user_exists(self, email: str, session: AsyncSession):
        """
        Check if a user exists in the database by their email address.

        Args:
            email (str): The email address to check for existence.
            session (AsyncSession): The asynchronous database session for
            executing queries.

        Returns:
            bool: True if the user exists; otherwise, False.
        """
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False

    async def get_all_users(self, session: AsyncSession):
        """
        Retrieve all users from the database, ordered by creation date (newest first).

        Args:
            session (AsyncSession): The asynchronous database session for
            executing queries.

        Returns:
            list[UserModel]: A list of all user objects in the database.
        """
        statement = select(UserModel).order_by(desc(UserModel.created_at))
        result = await session.exec(statement)
        return result.all()

    async def create_user(
        self, user_data: UserCreateModel, session: AsyncSession
    ):
        """
        Create a new user in the database.

        Args:
            user_data (UserCreateModel): The user data to create the user,
            including name, email, and password.
            session (AsyncSession): The asynchronous database session for
            executing queries.

        Returns:
            UserModel: The newly created user object.
        """
        user_data_dict = user_data.model_dump()
        new_user = UserModel(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data.password)
        session.add(new_user)
        await session.commit()
        return new_user
