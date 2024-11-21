from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.auth.schema import UserCreateModel, UserLoginModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService
from src.auth.utils import create_access_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse

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
    return {
        "message": "User created successfully."
    }


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
async def login_user(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        if verify_password(password, user.password_hash):
            token = create_access_token(
                user_data={
                    "email": email,
                    "user_uid": str(user.uid),
                }
            )
            refres_token = create_access_token(
                user_data={
                    "email": email,
                    "user_uid": str(user.uid),
                },
                expiry=timedelta(days=7),
                refresh=True
            )
            return JSONResponse(
                content={
                    "message": "Login successful.",
                    "access_token": token,
                    "refresh_token": refres_token,
                    "user": {
                        "uid": str(user.uid),
                        "email": user.email,
                        "username": user.username,
                    }
                }
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password."
    )
