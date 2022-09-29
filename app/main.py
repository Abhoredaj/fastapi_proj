from fastapi.middleware.cors import CORSMiddleware
from app.routers import post, user, auth, vote
from app.database import engine
from fastapi.params import Body
from app.config import settings
from fastapi import FastAPI
from email import message
from turtle import title
from app import models


#models.Base.metadata.create_all(bind=engine)
#I have commented it out because now every thing is worked out by alembic ;-)
app = FastAPI()
#CORSMiddleware is used when two api's are running on different domain so that the communication does not got interrupted as many of 
#api's are generated from web browsers having different domain.
origins = ["*"]#Origins is list of strings which are of URL type in which our api's run if it is "*" then it means it can run in any public domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "world"}



