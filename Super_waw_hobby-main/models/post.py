from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), index=True)
    hobby_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    # УБРАЛИ ВСЕ RELATIONSHIP ВРЕМЕННО, ЧТОБЫ РАЗОРВАТЬ ЦИКЛ
    # likes = relationship("Like", back_populates="post")
    # comments = relationship("Comment", back_populates="post")
    # reposts = relationship("Repost", back_populates="post")
    # user = relationship("User", back_populates="posts")
    # post_tags = relationship("Tag", secondary="post_tags", back_populates="posts")