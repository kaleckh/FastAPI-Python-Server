from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Table,
    JSON,
    create_engine,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, UTC
from sqlalchemy.types import TypeDecorator
from app.database import Base
from datetime import datetime
from cuid import cuid

engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

user_followers_table = Table(
    "user_followers",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("follower_id", String, ForeignKey("users.id"), primary_key=True),
)


class ArrayOrJson(TypeDecorator):
    impl = ARRAY

    def load_dialect_impl(self, dialect):
        if dialect.name == "sqlite":
            return dialect.type_descriptor(JSON())  
        return dialect.type_descriptor(ARRAY(String)) 

    def process_bind_param(self, value, dialect):
        if dialect.name == "sqlite":
            return value  
        return value  

    def process_result_value(self, value, dialect):
        if dialect.name == "sqlite":
            return value 
        return value  


class Post(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True, default=lambda: cuid())
    content = Column(String, nullable=True)
    email = Column(String, ForeignKey("users.email"), nullable=True)
    username = Column("username", String, nullable=False)
    likes = Column(ArrayOrJson(String), default=list)
    comments = relationship("Comment", back_populates="post")
    date = Column(DateTime, default=lambda: datetime.now(UTC))
    owner = relationship("User", back_populates="posts")
    reposts = relationship("Repost", back_populates="post")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: cuid())
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    reposts = relationship("Repost", back_populates="user")
    date = Column(DateTime, default=lambda: datetime.now(UTC))
    blurhash = Column(String, nullable=True)
    location = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    color = Column(String, nullable=True)
    links = Column(String, nullable=True)
    followers = Column(ArrayOrJson(String), default=list)
    following = Column(ArrayOrJson(String), default=list)
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="user")
    conversations = relationship("UsersInConversations", back_populates="user")
    messages = relationship("Message", back_populates="user")


class Repost(Base):
    __tablename__ = "reposts"
    id = Column(String, primary_key=True, default=lambda: cuid())
    post_id = Column(String, ForeignKey("posts.id", ondelete="CASCADE"), nullable=True)
    comment_id = Column(
        String, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True
    )
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(UTC))
    post = relationship("Post", back_populates="reposts")
    comment = relationship("Comment", back_populates="reposts")
    user = relationship("User", back_populates="reposts")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: cuid())
    messages = relationship("Message", back_populates="conversation")
    date = Column(DateTime, default=lambda: datetime.now(UTC))
    users = relationship("UsersInConversations", back_populates="conversation")


class UsersInConversations(Base):
    __tablename__ = "users_in_conversations"

    conversation_id = Column(
        String, ForeignKey("conversations.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    conversation = relationship("Conversation", back_populates="users")
    user = relationship("User", back_populates="conversations")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: cuid())
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"))
    date = Column(DateTime, default=lambda: datetime.now(UTC))
    message = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    status = Column(String, nullable=True)
    conversation = relationship("Conversation", back_populates="messages")
    user = relationship("User", back_populates="messages")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True, default=lambda: cuid())
    content = Column(String, nullable=False)
    post_id = Column(String, ForeignKey("posts.id", ondelete="CASCADE"))
    likes = Column(ArrayOrJson(String), default=list)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    username = Column(String, nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(UTC))
    parent_id = Column(String, ForeignKey("comments.id"), nullable=True)
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
    reposts = relationship("Repost", back_populates="comment")
