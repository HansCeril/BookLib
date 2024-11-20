from passlib.context import CryptContext

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
