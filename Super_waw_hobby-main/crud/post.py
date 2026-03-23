from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Post, Like, Comment, Repost, Tag, PostTag
from ..schemas import PostCreate, PostUpdate, PostRead

def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(**post.dict(exclude={"tag_ids"}), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    if post.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(post.tag_ids)).all()
        for tag in tags:
            db.add(PostTag(post_id=db_post.id, tag_id=tag.id))
        db.commit()
        db.refresh(db_post)

    return db_post

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session):
    posts = db.query(Post).all()
    for p in posts:
        p.likes_count = db.query(func.count(Like.id)).filter(Like.post_id == p.id).scalar()
        p.comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == p.id).scalar()
        p.reposts_count = db.query(func.count(Repost.id)).filter(Repost.post_id == p.id).scalar()
    return posts

def update_post(db: Session, db_post: Post, post_update: PostUpdate):
    update_data = post_update.dict(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)

    for key, value in update_data.items():
        setattr(db_post, key, value)

    if tag_ids is not None:
        db.query(PostTag).filter(PostTag.post_id == db_post.id).delete()
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        for tag in tags:
            db.add(PostTag(post_id=db_post.id, tag_id=tag.id))

    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()