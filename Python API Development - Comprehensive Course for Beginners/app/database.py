from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "dialect+driver://username:password@host:port/database"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://bob:password123@localhost/products_db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://xxxx:yyyy@localhost/zzzz"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
