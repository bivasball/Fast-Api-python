
from fastapi import  Response, status, HTTPException, APIRouter, Depends
from typing import  List
import  time
import psycopg2
import psycopg2.extras
from ..schemas import DataModel
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from pydantic import BaseModel

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


my_posts = [
    {"title": "mr", "content": "myschool days", "id": 1},
    {"title": "mrs Elot", "content": "i am wealtier", "id": 2},
    {"title": "Sir braddmaon", "content": "In a summber dar", "id": 3}
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
"""
try:
        #establishing the connection
    conn = psycopg2.connect(
    database="tatai", user='postgres', password='root@123', host='127.0.0.1', port='5432',cursor_factory=psycopg2.extras.RealDictCursor )
    # create a cursor
    cur = conn.cursor()
    print("connected to database")
except Exception as error:
    print("Error while connecting to PostgreSQL", error)
    print("Error",error )
    time.sleep(5)
    print("Retrying connection...")
"""


@router.post("/")
async def receive_data22(payload: DataModel):
    print("===============")
    print(payload.model_dump())
    mypp = payload.model_dump()
    mypp['rating'] = random.randint(1, 1000)
    my_posts.append(mypp)
    return {"message": "Request received", "data": my_posts}


#@router.get("/")
#@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.PostBase])
async def root2():
    postt = my_posts
    return postt

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def rootdelete(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def toupdate(id: int,post: DataModel):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index]= post_dict
    return { "message": "Updated successfully","data": post_dict}


#---------------------copied from Snjv--------------------------#
@router.get("/",status_code=status.HTTP_200_OK)
async def receive_datafromDb(db: Session = Depends(get_db),):
    
    # Explicitly wrap the SQL query in text()
    result = db.execute(text("SELECT * FROM fast_api.products"))
    
    # Use `.mappings()` to convert rows into dictionaries
    posts = result.mappings().all()
    results = [dict(row) for row in posts]
    print(results)

    postt = my_posts
    return results
    


# Define the Pydantic model for request validation
class ProductCreate122(BaseModel):
    name: str
    price: int
    is_sale: bool
    inventory: int
    
    class Config:
        from_attributes = True  # Replace from_attributes
        
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product_and_save_to_Db(product: ProductCreate122, db: Session = Depends(get_db)):
    print("Received Data:", product.model_dump())  # Debugging step
    try:
        query = text("""
            INSERT INTO fast_api.products (name, price,is_sale, inventory)
            VALUES (:name, :price, :is_sale, :inventory) RETURNING id
        """)

        result = db.execute(query, {
            "name": product.name,
            "price": product.price,           
            "is_sale": product.is_sale,
            "inventory": product.inventory
        })

        db.commit()  # Commit changes to the database
        new_product_id = result.scalar()

        return {"message": "Product created successfully", "id": new_product_id}

    except Exception as e:
        db.rollback()  # Rollback in case of errors
        raise HTTPException(status_code=500, detail=str(e))
