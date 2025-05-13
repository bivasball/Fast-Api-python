from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_USERNAME,DATABASE_PASSWORD, DATABASE_HOSTNAME,DATABASE_PORT, DATABASE_NAME


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

# Create the database engine with SQLAlchemy 2.0 best practices
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

# Create a session factory using SQLAlchemy 2.0 style
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# Use DeclarativeBase instead of declarative_base (SQLAlchemy v2 update)
class Base(DeclarativeBase):
    pass

# Dependency to get a database session
def get_db():
    with SessionLocal() as db:
        yield db
