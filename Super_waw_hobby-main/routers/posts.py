from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database import get_db
from models import Post, Like, Repost, Tag
from schemas.post import PostCreate, PostRead, TagRead

router = APIRouter(prefix="/posts", tags=["Посты"])

@router.get("/", response_model=List[PostRead], summary="Лента всех постов")
def получить_ленту(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    result = []
    for post in posts:
        data = PostRead.from_orm(post)
        data.user_username = "testuser"  # хардкод
        data.user_photo = None
        data.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar() or 0
        data.comments_count = 0  # пока без комментариев
        data.reposts_count = db.query(func.count(Repost.id)).filter(Repost.post_id == post.id).scalar() or 0
        data.tags = [TagRead(id=t.id, name=t.name) for t in post.post_tags]
        result.append(data)
    return result

@router.post("/", response_model=PostRead, summary="Создать новый пост")
def создать_пост(post_in: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(
        title=post_in.title,
        content=post_in.content,
        image_url=str(post_in.image_url) if post_in.image_url else None,
        hobby_done=post_in.hobby_done,
        user_id=1  # хардкод
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    for tag_id in post_in.tag_ids:
        tag = db.query(Tag).get(tag_id)
        if tag:
            db_post.post_tags.append(tag)

    db.commit()
    db.refresh(db_post)

    data = PostRead.from_orm(db_post)
    data.user_username = "testuser"
    data.user_photo = None
    data.tags = [TagRead(id=t.id, name=t.name) for t in db_post.post_tags]
    return data

@router.post("/{post_id}/like", summary="Поставить/убрать лайк")
def лайкнуть_пост(post_id: int, db: Session = Depends(get_db)):
    like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == 1).first()
    if like:
        db.delete(like)
        db.commit()
        return {"сообщение": "Лайк убран"}
    db.add(Like(post_id=post_id, user_id=1))
    db.commit()
    return {"сообщение": "Лайк поставлен"}

@router.post("/{post_id}/repost", summary="Сделать репост")
def репостнуть_пост(post_id: int, db: Session = Depends(get_db)):
    existing = db.query(Repost).filter(Repost.post_id == post_id, Repost.user_id == 1).first()
    if existing:
        return {"сообщение": "Уже репостнул"}
    db.add(Repost(post_id=post_id, user_id=1))
    db.commit()
    return {"сообщение": "Репост сделан"}

@router.get("/liked", response_model=List[PostRead], summary="Посты, которые я лайкал")
def мои_лайкнутые(db: Session = Depends(get_db)):
    liked = db.query(Post).join(Like).filter(Like.user_id == 1).all()
    result = []
    for post in liked:
        data = PostRead.from_orm(post)
        data.user_username = "testuser"
        data.user_photo = None
        data.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar() or 0
        data.tags = [TagRead(id=t.id, name=t.name) for t in post.post_tags]
        data.is_liked_by_me = True
        result.append(data)
    return result