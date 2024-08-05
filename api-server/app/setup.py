from app.core.database import Base, SessionLocal, engine
from app.models import User
from app.repositories import user_repo
from app.schemas import UserCreate


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "a").first()
        if not user:
            user_in = UserCreate(username="a", password="a", email="a@gmail.com")
            user_repo.create_user(db=db, user=user_in, is_admin=False)
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
