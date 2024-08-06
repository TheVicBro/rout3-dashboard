import random
import string
from datetime import datetime

from app.core.database import Base, SessionLocal, engine
from app.models import Myapi, Secret, User
from app.repositories import myapi_repo, secrets_repo, user_repo
from app.schemas import MyApiCreate, SecretCreate, UserCreate
from app.services import myapi


def generate_random_name(length=8):
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def init_db(num_myapi_keys=3):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Create user if it does not exist (this will be moved later to settings)
        user = db.query(User).filter(User.username == "a").first()
        if not user:
            user_in = UserCreate(username="a", password="password", email="a@gmail.com")
            user = user_repo.create_user(db=db, user=user_in, is_admin=False)

        # Create secrets for specified providers
        secret_names = ["openai", "cohere", "anthropic", "google"]
        for secret_name in secret_names:
            secret = db.query(Secret).filter(Secret.name == secret_name).first()
            if not secret:
                secret_in = SecretCreate(
                    name=secret_name,
                    last_used=datetime.now(),
                    key=myapi.generate_api_key(),
                )
                secrets_repo.create_secret(db=db, secret=secret_in, user_id=user.id)

        # Create or update myapi keys
        existing_myapi_keys = db.query(Myapi).filter(Myapi.user_id == user.id).all()

        # Add new keys if there are fewer than num_myapi_keys
        keys_to_add = num_myapi_keys - len(existing_myapi_keys)
        for _ in range(max(0, keys_to_add)):
            myapi_key_in = MyApiCreate(
                name=generate_random_name(), key=myapi.generate_api_key()
            )
            myapi_repo.create_myapi(
                db=db,
                myapi_key=myapi_key_in.key,
                name=myapi_key_in.name,
                user_id=user.id,
            )

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
