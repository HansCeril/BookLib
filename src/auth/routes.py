from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.auth.schema import UserCreateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService


auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )
    await user_service.create_user(user_data, session)
    return {"message": "User created successfully."}
