from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a password matches the hash."""
    return pwd_context.verify(plain_password, hashed_password)