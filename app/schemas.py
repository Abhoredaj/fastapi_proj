from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime  import datetime
from typing import Optional

#Pydantic model is used for user validation as well as for the conversion of dictionary to json
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostCount(BaseModel):
    post_count: int

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
#As in response in frontend we do not want user to show the user what his password is therefore we do not include password in response
#Similarly as "Post" response we want our response in pydentic not in sql alchemy therefore adding class "Config"
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    #The above code is helpful in giving response from what we want to give to the frontend
    class Config:#The cause of writing this is here the output or response is in the form of sql alchemy but
        orm_mode = True#We want our response or output in function's return in the form of pydentic
        #If we don't do this causes error
        
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    #If we want to embed id in ascess token 

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)