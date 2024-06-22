from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(plaintext_password: str):
    return pwd_context.hash(plaintext_password)


def verify_password(plaintext_password, hashed_password):
    return pwd_context.verify(plaintext_password, hashed_password)


def authenticate_user(password, hashed_password):
    return pwd_context.verify(password, hashed_password)
