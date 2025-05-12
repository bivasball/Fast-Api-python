from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Define the database URL using environment variables
#SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Define the database URL using environment variables
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:root%40123@127.0.0.1:5432/tatai"




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
