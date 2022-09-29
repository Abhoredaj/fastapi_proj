from turtle import title
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    title: str
    Genre: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"Hello": "world"}
#Creating a pydentic model
@app.post("/createposts")
def create_pots(post: Post):
    print(post.title)
    print(post.published)
    print(post.rating)
    print(post.dict())
    return {"data": post}