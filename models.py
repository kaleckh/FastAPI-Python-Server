from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Table, JSON
from sqlalchemy.orm import relationship, backref
from database import Base
from datetime import datetime
from cuid2 import Cuid as cuid

# Many-to-Many association tables
post_voted_table = Table(
    'post_voted', Base.metadata,
    Column('post_id', String, ForeignKey('posts.id')),
    Column('user_id', String, ForeignKey('users.id'))
)

post_likes_table = Table(
    'post_likes', Base.metadata,
    Column('post_id', String, ForeignKey('posts.id')),
    Column('user_id', String, ForeignKey('users.id'))
)

post_dislikes_table = Table(
    'post_dislikes', Base.metadata,
    Column('post_id', String, ForeignKey('posts.id')),
    Column('user_id', String, ForeignKey('users.id'))
)

user_followers_table = Table(
    'user_followers', Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('follower_id', String, ForeignKey('users.id'))
)

user_following_table = Table(
    'user_following', Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('following_id', String, ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: cuid())
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    bio = Column(String)
    blurhash = Column(String)
    posts = relationship('Post', back_populates='owner')
    votes = relationship('Vote', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    bookmarks = relationship('Bookmark', back_populates='user')
    followers = relationship("User",
                             secondary=user_followers_table,
                             primaryjoin=id == user_followers_table.c.user_id,
                             secondaryjoin=id == user_followers_table.c.follower_id,
                             backref="following")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(String, primary_key=True, default=lambda: cuid())
    title = Column(String, nullable=False)
    content = Column(String)
    thesis = Column(String)
    yes_action = Column(String)
    maybe_action = Column(String)
    no_action = Column(String)
    categories = Column(JSON)  # Storing array data as JSON
    voted = relationship("User", secondary=post_voted_table)
    likes = relationship("User", secondary=post_likes_table)
    dislikes = relationship("User", secondary=post_dislikes_table)
    comments = relationship('Comment', back_populates='post')
    vote_records = relationship('Vote', back_populates='post')
    bookmarks = relationship('Bookmark', back_populates='post')
    date = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(String, ForeignKey('users.id'))
    owner = relationship("User", back_populates="posts")


class Vote(Base):
    __tablename__ = 'votes'

    id = Column(String, primary_key=True, default=lambda: cuid())
    vote = Column(String)
    user_id = Column(String, ForeignKey('users.id'))
    post_id = Column(String, ForeignKey('posts.id'))
    user = relationship('User', back_populates='votes')
    post = relationship('Post', back_populates='vote_records')


class Bookmark(Base):
    __tablename__ = 'bookmarks'

    id = Column(String, primary_key=True, default=lambda: cuid())
    user_id = Column(String, ForeignKey('users.id'))
    post_id = Column(String, ForeignKey('posts.id'))
    user = relationship('User', back_populates='bookmarks')
    post = relationship('Post', back_populates='bookmarks')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(String, primary_key=True, default=lambda: cuid())
    comment = Column(String, nullable=False)
    vote = Column(String)
    likes = Column(JSON)
    dislikes = Column(JSON)
    post_id = Column(String, ForeignKey('posts.id'))
    user_id = Column(String, ForeignKey('users.id'))
    username = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    parent_id = Column(String, ForeignKey('comments.id'))
    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')
    parent = relationship('Comment', remote_side=[id], backref="replies")


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(String, primary_key=True, default=lambda: cuid())
    me = Column(String)
    room_name = Column(String)
    recipient = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    messages = relationship('Message', back_populates='conversation')


class Message(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True, default=lambda: cuid())
    conversation_id = Column(String, ForeignKey('conversations.id'))
    date = Column(DateTime, default=datetime.utcnow)
    message = Column(String, nullable=False)
    user_name = Column(String)
    status = Column(String)
    recipient = Column(String)
    conversation = relationship('Conversation', back_populates='messages')
