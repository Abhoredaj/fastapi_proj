from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials:  OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #OAuth2PasswordRequestForm email id username(dictionary) ke form mai leta tabhi hum "user_credentials.username" likhte hai
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#'''user = db.query(models.User).filter(models.User.email == user_credentials.username).first()'''
#In the above line of code we are just try to match the login user and password 
#But not making the acess token or jwt token
#Creating token is just to make session used in the front end so we do not need the database in the backend 
    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})#"user.id" is used to send for the making of the payload in the oauth2 file function 
    #In place of user id you can pass any thing but the payload should be small so it doesnot exhaust the bandwith
    # jab aapka password verification ho jaata hai phir fastapi secret key,header and payload ka use kar ke signature banata hai
    #phir wo signature,header and payload ka use kar ke access_token banata hai and hume woh token send kardeta hai
    #phir hum token ke sath post id bhi send karte hai jiska hume post ya data chahiye
    #phir se fastapi token ke signature ka verification karta hai taake third partyne token ke sath chedchad to nhi kiya
    # This the reason we use token  
    return {"access_token": access_token, "token_type": "bearer"}