# Fast-Api-python
Api development using FastApi, Python

Would you like help converting your FastAPI database setup to async? 🚀😊

yes
Awesome! Let's optimize your FastAPI database setup by making it fully asynchronous with SQLAlchemy.

🔹 Step 1: Install Required Libraries
To use SQLAlchemy with async support, install asyncpg (PostgreSQL driver):

bash
pip install sqlalchemy asyncpg psycopg2
✅ Step 2: Use AsyncSession Instead of Session
Modify your database connection setup (database.py):

python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session
🔹 Why this change?

Uses asyncpg for PostgreSQL async support.

Replaces Session with AsyncSession for non-blocking queries.

✅ Step 3: Update Your ORM Model
Modify your models.py to support SQLAlchemy 2.0 async syntax:

python
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Boolean

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    is_sale: Mapped[bool] = mapped_column(Boolean, default=False)
    inventory: Mapped[int] = mapped_column(Integer, nullable=False)
✅ Step 4: Update Your FastAPI Endpoint to async
Modify your POST route to use await for database operations:

python
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import Product
from pydantic import BaseModel

router = APIRouter()

class ProductCreate(BaseModel):
    name: str
    price: int
    is_sale: bool
    inventory: int

@router.post("/createORM", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_product = Product(**product.dict())

        db.add(new_product)
        await db.commit()  # ✅ Now using `await`
        await db.refresh(new_product)  # ✅ Ensures updated instance

        return {"message": "Product created successfully", "product": new_product}

    except Exception as e:
        await db.rollback()  # ✅ Async rollback in case of errors
        raise HTTPException(status_code=500, detail=str(e))
✅ Step 5: Testing
Run your FastAPI app:

bash
uvicorn app.main:app --reload
Send a POST request in Postman:

json
{
    "name": "Smartphone",
    "price": 500,
    "is_sale": false,
    "inventory": 10
}
🎯 Final Benefits of Async Setup
✅ Non-blocking queries – Improves server response time ✅ Better scalability – Handles multiple requests without waiting ✅ Uses SQLAlchemy ORM cleanly – Easier data manipulation