from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.celery_worker import get_count_all_posts
from app import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/{id}", response_model=schemas.PostOut)#Here we are getting id in string type
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):#Here two things happening 1st is converting numeric string to integer and 
    #2nd is using pydantic we get good validation that user use only numeric string and does not user the alphabet string if we do not use we 
    # get the internal error on postman  
    #cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    #post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()#"filter" is used instead of "WHERE"
    #".first()"It is used to take the first id and do not check for all rows of ID column
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")     

    #if post.owner_id != current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            #detail="Not authorized to perform requested action")   
        #response.status_code = status.HTTP_404_NOT_FOUND
        #THE ABOVE LINE OF CODE IS USED MOSTLY FoR INSTAGRAM TYPE OR FACEBOOK TYPE
        #return {'message': f"post with id: {id} does not exist"}
    return post

    
@router.get("/", response_model=List[schemas.PostOut])
#For giving response to the frontend in decorater "@app.get("/posts")" this piece of code 
#"response_model=schemas.Post" does not work reason is simple because the response here we get all the values in the database
#but by using commented code gives output in one form so this cause error
#So we have to use "from typing import List" to type cast responses in form of List
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):#"db: Session = Depends(get_db)" is used to make sqlalchemy to make session to connect with database
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #Here limit is sql parameter how much user wanted the getpost to be loaded
    print(limit)
    #posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).limit(limit).all()"This line of code is used when the user wanted to read his own post like personal so this is not useful for twitter like appliction"
    #posts = db.query(models.Post).filter( 
       # models.Post.title.contains(search)).limit(limit).offset(skip).all()
       #THe above line of code is for getting posts but without votes or "LIKES"

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get('/count/{id_}', response_model=schemas.PostCount)
def get_post_count(id_: int, current_user: int = Depends(oauth2.get_current_user)):
    result = get_count_all_posts(id_)
    print(result)
    return {"post_count" : result}
#Hum yaha par koi bhi sql alhemy model jo database model ke form mai hai wo pass nhi kar rahe hai
#Isliye humein jo return hai wo ek dictionary bole to pydentic ke term par rakhna hai yaad se 


#Creating a pydentic model
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #ye jo "current_user" functon means "oauth2.get_current_user" add kiya hai "create_posts" function ke parameter mai
    # Iska reason ye hai ki jab user token ke sath user_ID resend karega to fastapi verify karega ki bhai token same hai ki nhi ya kuch usme 
    #changes hua hai
    #Do not use the "f" string because it makes the code vulnerable to the dbms attacks from fast api tutorial video
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                    #(post.title, post.content, post.published))
    #new_post = cursor.fetchone()

    #conn.commit()#commit is used to save the changes in the database
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())#models.Post(title=post.title, content=post.content, published=post.published)
    #"**post.dict()" is used in place of "title=post.title, content=post.content, published=post.published" of all this
    #Because there may be the case where we have more than 20 columns so writing all this regularly causes hectic
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#Here refresh is used for "RETURNING *"
    return new_post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")  

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)#response_model gives output to frontend
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                 #(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")        
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()