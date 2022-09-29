from celery import Celery
from celery.utils.log import get_task_logger
from app import database, models
from sqlalchemy import func


#celery -A celery_worker.celery worker --pool=solo --loglevel=info

celery = Celery('tasks', backend="amqp", broker='amqp://guest:guest@127.0.0.1:5672//')

celery_log = get_task_logger(__name__) 

db = database.SessionLocal()


@celery.task()
def get_count_all_posts(id_):
    celery_log.info("fetching all posts")
    print(id_)
    posts = db.query(models.Post).filter(models.Post.owner_id==id_).all()
    celery_log.info("capturing the count")
    print(posts)
    count = len(posts)
    print(count)
    return count
    #return posts
