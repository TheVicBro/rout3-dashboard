from datetime import datetime

from app.core.database import Base, SessionLocal, engine
from app.models import Myapi, Secret, User
from app.repositories import myapi_repo, secrets_repo, user_repo
from app.schemas import MyApiCreate, SecretCreate, UserCreate
from app.services import myapi


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Create user if it does one does not exist
        user = db.query(User).filter(User.username == "a").first()
        if not user:
            user_in = UserCreate(username="a", password="a", email="a@gmail.com")
            user = user_repo.create_user(db=db, user=user_in, is_admin=False)

        # Create a secret
        secret = db.query(Secret).filter(Secret.name == "openai").first()
        if not secret:
            secret_in = SecretCreate(
                name="openai", last_used=datetime.now(), key=myapi.generate_api_key()
            )
            secrets_repo.create_secret(db=db, secret=secret_in, user_id=user.id)

        # Create a myapi key
        myapi_key = db.query(Myapi).filter(Myapi.name == "myap").first()
        if not myapi_key:
            myapi_key_in = MyApiCreate(name="myapi", key=myapi.generate_api_key())
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
