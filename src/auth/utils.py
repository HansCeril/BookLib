from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import config
import jwt
import uuid
import logging


pwd_context = CryptContext(
    schemes=["bcrypt"]
)


def generate_password_hash(password: str) -> str:
    """_summary_

    Generate a secure hash for a given password.

    This function takes a plain text password and generates a hashed version
    using the password context (bcrypt hashing algorithm).
    The hash can be stored in a database for later verification.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password as a string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """_summary_

    Verify a plain text password against a hashed password.

    This function takes a plain text password and a hashed password and
    verifies that the plain text password matches the hashed password.

    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password to be verified against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_data: dict,
    expiry: timedelta = None,
    refresh: bool = False
) -> str:
    """
    Generate a JSON Web Token (JWT) for user authentication.

    Args:
        user_data (dict): A dictionary containing user information.
                          Must include the "email" key for the token's subject.
        expiry (timedelta, optional): The expiration time of the token.
                                      If not provided, defaults to the
                                      configured JWT expiration time in
                                      seconds.
        refresh (bool, optional): Indicates whether the token is a
                                  refresh token. Defaults to False.

    Returns:
        str: The encoded JWT as a string.

    Notes:
        - The token payload includes:
            - "sub": The email of the user (subject).
            - "exp": The expiration time.
            - "jti": A unique identifier for the token.
            - "refresh": A flag indicating if the token is a refresh token.
        - The token is signed using the secret key and algorithm
          specified in the configuration.
    """
    token = jwt.encode(
        payload={
            "sub": user_data.get("email"),
            "exp": (
                datetime.now() + (
                    expiry if expiry is not None
                    else timedelta(seconds=config.JWT_EXPIRATION_TIME_SECONDS)
                )
            ),
            "jti": str(uuid.uuid4()),
            "refresh": refresh
        },
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )
    return token


def decode_token(token: str) -> dict:
    """
    Decode a JSON Web Token (JWT) and return its payload.

    Args:
        token (str): The encoded JWT to be decoded.

    Returns:
        dict: The decoded token payload as a dictionary.

    Notes:
        - The token payload includes:
            - "sub": The email of the user (subject).
            - "exp": The expiration time.
            - "jti": A unique identifier for the token.
            - "refresh": A flag indicating if the token is a refresh token.
    """
    try:
        token_data = jwt.decode(
            jwt=token,
            key=config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWKError as e:
        logging.exception(f"Error decoding token: {e}")
        raise jwt.PyJWKError(f"Error decoding token: {e}")
    except jwt.ExpiredSignatureError as e:
        logging.exception(f"Token has expired: {e}")
        raise jwt.ExpiredSignatureError(f"Token has expired: {e}")
    except jwt.InvalidTokenError as e:
        logging.exception(f"Invalid token: {e}")
        raise jwt.InvalidTokenError(f"Invalid token: {e}")
