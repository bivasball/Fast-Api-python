from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()
class DataModel(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None
    id: Optional[int] = None

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

@app.post("/fetchData")
async def receive_data22(payload: DataModel):
    print("===============")
    print(payload.dict())
    mypp = payload.dict()
    mypp['rating'] = random.randint(1, 1000)
    my_posts.append(mypp)
    return {"message": "Request received", "data": my_posts}

@app.post("/submit")
async def receive_data(payload: DataModel):
    print("===============")
    print(payload.dict())
    return {"message": "Data received", "data": payload}

@app.get("/")
async def root1():
    return {"message": "Hello World Dear now are you? sourrav sarkar"}

@app.get("/posting")
async def root2():
    postt = my_posts
    return {"postdetails": postt}

@app.post("/postHere")
async def myPostApi(payload: dict=  Body(...)):
   
    print(payload)
    return {"message": "Thanks for posting", "data": payload}

@app.get("/postingr/{id}")
async def root2r(id: int,response:Response):
    post = find_post(id)
    print(post)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Post not found"}
    return {"postdetails": post}

@app.get("/posting_mod/{id}")
async def root2r(id: int):
    post = find_post(id)
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"postdetails": post}

@app.delete("/postdelete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def rootdelete(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/update/{id}")
async def toupdate(id: int,post: DataModel):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index]= post_dict
    return { "message": "Updated successfully","data": post_dict}
