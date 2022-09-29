from email import message
from turtle import title
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()

class Post(BaseModel):#Pydantic model is used for user validation as well as for the conversion of dictionary to json
    title: str
    Genre: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of the book", "Genre": "Genre of the book", "id": 1}, {"title": "Harry_potter", "Genre": "Animation", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.get("/posts/latest")#This is for latest post
def get_posts():#This should be above "posts/{id}" because fastapi get confused
    post = my_posts[len(my_posts)-1]#this request with the "posts/{id}"
    return {"data": post}#Because order matters

@app.get("/posts/{id}")#Here we are getting id in string type
def get_posts(id: int):#Here two things happening 1st is converting numeric string to integer and 
    #2nd is using pydantic we get good validation that user use only numeric string and does not user the alphabet string if we do not use we 
    # get the internal error on postman  
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")        
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id: {id} does not exist"}
    print(post)
    return {"post_detail": post}

    
@app.get("/posts")
def get_posts():
    return {"data": my_posts}


#Creating a pydentic model
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(post.title)
    print(post.published)
    print(post.rating)
    post_dict = post.dict()#convert pydentic to dictionary
    post_dict['id'] = randrange(0,100000000)
    my_posts.append(post_dict)
    return {"data": post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_posts(id: int): 
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")        
        
    my_posts.pop(index)
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")        
        
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict 
    return {"data": post_dict}