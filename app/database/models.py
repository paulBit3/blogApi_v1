# this class managing our entity

#from flask_bcrypt import bcrypt, generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash, generate_password_hash
from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField, IntField, BooleanField
from datetime import datetime

from .db_init import db


""" Post class model
We created a method to convert a post instance into a dictionary 
format suitable for MongoDB storage.
We defined a static method to create a post instance from a dictionary

Converting Post instances to dictionary format allows us to smoothly interaction with our MongoDB database'
"""

""" User class model
    This class manages user details
"""

class User(Document):
    user_id = IntField(blank=True, null=True, primary_key=True, auto_increment = True)
    username = StringField(required=True, max_length=30, unique=True)
    password = StringField(required=True, max_length=300, nullable=False, unique=True)
        
    post = ListField(ReferenceField('Post'))
 
    def __repr__(self):
        return self.username
        
    def __str__(self, username, user_id):
        self.username = username.upper()
        self.user_id = user_id

    #convert data in bson object
    def to_bson(self):
        data = dict()
        #data = self.data_dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data
    

    #hashing our password by bcrypt
    def hashed_password(self, secret:str):
        self.password = generate_password_hash(secret)
    
    #checking if the generated pw == to the one saved in the Database
    def check_password(self, password):
        return check_password_hash(str(self.password), password)


class Post(Document):
    post_id = StringField(blank=True, null=True, primary_key=True)
    title = StringField(required=True, max_length=50)
    author = ReferenceField(User, required=True)
    content = StringField(max_length=255, required=True)
    posted = BooleanField(default = False)
    read_time = StringField(required=True)
    read_count = IntField(default = 0)
    posted_at = DateTimeField(default=datetime.now().timestamp())

    #convert a post instance into a dictionary
    def conv_post_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "posted_at": self.posted_at,
            "post_id": self.post_id
        }

    # create a Post instance. it takes a post data as param 
    def post_instance(post):
        return Post(
            title= post.get('title'),
            author = post.get('author'),
            content = post.get('content'),
            post_id = post.get('post_id')
        )
    
    """
     returning string representation. __repr__ return a string 
     containing a printable representation of an object which is useful for serialization and debugging.
    """
    def __repr__(self):
        return self.title, self.author, self.posted_at
    
    def __str__(self):
        return self.title, self.author, self.posted_at




#if a user is deleted then the post created by the user is also deleted.
User.register_delete_rule(Post, 'author', db.CASCADE)

           

            