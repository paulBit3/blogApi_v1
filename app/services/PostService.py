"""
 I defined this service class to manage our post service api
"""
import os
from flask import jsonify
from bson.objectid import ObjectId
from pymongo import ASCENDING, MongoClient

from database.uri import URI



#db uri
db_uri = URI.MONGO_DB_URI
client = MongoClient(db_uri)

#connecting to the database
db = client.get_database('Blog')
db = client.Cluster0
blog = db.blog

#post collection. you could also uncomment post_collection. that will create a Post collection object in the Db 
#post_col = db.get_collection('Post')

#blog collection.
blog_col = db.get_collection('blogData')

error = None


#method to insert a new post
def add_post(post_obj):
    """Add a new post"""
    #search for an existing post
    title = get_post_title(post_obj)
    post = get_by_user_id_and_title(post_obj, title)

    #if a post nots exist create a new one
    if not post:
        return blog_col.insert_one(post_obj)
     


""" method to display all posted posts(assuming that user can save a post as draft and pick it up later, and 
posted after some time... so we will display only those posts wha have been posted instead.
in our DB we set an Enum field to handle that sate... 
we could also set a boolean field..but Enumfield is enough)"""
def list_posts():
    """Get a list of posts"""
    # we passed in a query that will get  only a sorted posts with  sort oder ASCENDING or DESCENDING
    #all_posts = post_col.find({Post.post_state:'Posted'}).sort('title', ASCENDING)
    
    #ASCENDING order from the first post
    return list(blog_col.find().sort('_id', ASCENDING))

    #DESCENDING order start from the last post
    #return list(blog_col.find().sort('_id', DESCENDING))
    


#method to update a single post
def update_post( post_id, title, content):
    """Update a post given its post_id"""
    
    _id = {"_id": ObjectId(post_id)}
    set_update_condition = {"$set": {"title": title, "content": content}}
    print(_id)
    return blog_col.update_one(_id, set_update_condition )

    #you can uncomment this if you want to use a Post collection instead
    #return post_col.update_one(post_id, set_update_condition)
 
    


#delete a single post
def delete_post(post_id, user_id):
    """delete a post given its Id"""
    #response, del_post = post_col.delete_one(post_id)

    _id = {"_id": ObjectId(post_id)}
    
    print(post_id)
    print(user_id)
    #get the post of the current user
    post = get_by_user_id(user_id)
    #print(post)
    #if there is no post, inform user
    if not post:
        return {'message': 'Post not found'}, 404
    return blog_col.delete_one(post)
  


""""Utils methods"""

#get a post by title
def get_post_title(post_obj):
    """Get a post given its title"""
    #post = post_col.find_one({'title': post_obj})
    post = blog_col.find_one({'title': post_obj})
    if not post:
        return None
    return post


#get a post by Id
def get_post_by_Id(post_id):
    """Get a post given its post_id"""
    # post = post_col.find_one({'_id': ObjectId})
    post = blog_col.find_one({'_id': ObjectId(post_id)})
    if not post:
        return jsonify({'message': 'Post with this Id not exists!'})
    return post


#get post by author(user_id) and title
def get_by_user_id_and_title(user_id, title):
        """Get a post given its title and author"""
        post = blog_col.find_one({"author": user_id, "title": title})
        if not post:
            return
        post["_id"] = str(post["_id"])
        return post


#get post by author(user_id) only
def get_by_user_id(user_id):
        """Get a post given its author"""
        post = blog_col.find_one({"author": user_id})

        return post


#get post by author(user_id) and post_id
def get_by_user_id_and_post_id(post_id, user_id ):
        """Get a post given postId and author"""
        post = blog_col.find_one({ "_id": ObjectId(post_id) ,"author": user_id})
        return post



