from app.api.deps import SessionDep
from app.core.security import verify_password
from app.models import User
from app.repositories import user_repo


def authenticate_user(
    db: SessionDep, username: str, plain_password: str
) -> User | None:
    user = user_repo.get_user_by_username(db=db, username=username)

    # Ensure user exists
    if not user:
        return None

    # Check user password with db hashed password
    if not verify_password(
        plain_password=plain_password, hashed_password=str(user.hashed_password)
    ):
        return None
    return user
