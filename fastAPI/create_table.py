from database import Base, ENGINE
from models import User, Post, Comments, Tags, Likes, Followers, Messages, PostTags

Base.metadata.create_all(bind=ENGINE)
