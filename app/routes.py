import math
import os
import bson
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required, get_jwt_identity
from bson.objectid import ObjectId


from pymongo import MongoClient

#importing DB Uri
from database.uri import URI


#importing post service
from services.PostService import add_post, list_posts, get_post_by_Id, update_post, delete_post, get_by_user_id

"""
  User must login to be able to create, update, or delete blog posts.
  to achieve this we use the @jwt_required() decorator to check that
  #if user is logged in, we can also get is Id
    user_id = get_jwt_identity()

"""


# I used Blueprint to architect our App
routes = Blueprint("routes", __name__, url_prefix="/api/blog")



#db uri
db_uri = URI.MONGO_DB_URI
client = MongoClient(db_uri)

#connecting to the database
db = client.get_database('Blog')

#an instance of our blog db collection
#blogData: Collection = db.get_collection('blogData')
post_col = db.get_collection('Post')
user_col = db.get_collection('User')
blog_col = db.get_collection('blogData')
#print(post_col)
db = client.Cluster0
blog = db.blog




"""Blog Posts implementing methods."""




#create a post(""to create a post in our blog, a user need to login first"")
@routes.route('/post', methods=['GET', 'POST'])
@jwt_required()
def create_post():
    """User must be logged in to be able to create a post."""
    #if user is logged in, we can also get is Id
    user_id = get_jwt_identity()
   

    if request.method == 'POST':
        
        #body = request.get_json()
        title = request.get_json().get('title', '')
        author = user_id
        content = request.get_json().get('content', '')
        #get the post read time
        readTime = read_time_post(content)
         #post state
        posted = get_post_state(title)

        body = {'title': title, 'author': author,'content': content, 'posted': posted, 'readTime': readTime}
     
        #if all is ok... I call out addpost method from post service module to save post data
        if body:
            data = add_post(body)
            #data = blog.insert_one(body)
            return jsonify({
                'message': 'You posted',
                'post': body
            }), 201




#rerieve all blog posts(I call the listposts method from our PostService module). 
# users do not have to login to see others users posts. They can kjust see others users
#  posts and read it, but they need to login to create their own post. 
# So I commented jwt_required() method, to do so
@routes.get('/posts')
#@jwt_required()
def retrieve_all_post():
    response = list_posts()
    return {
        "message": "success",
        "posts": response
    }, 200




#get a single post. I converted post_id from string to ObjectId using bson
@routes.get('/post/<string:post_id>')
@jwt_required()
def get_single_post(post_id):
    #posts = blog.find_one({"_id": ObjectId(post_id)}) 
    post = get_post_by_Id(post_id)
    return jsonify({
        'message': 'success',
        'post': post
    }), 200



#Updating an existing post
@routes.put('/post/<string:post_id>/edit')
@jwt_required()
def update_a_post(post_id):
    """User must be logged in to be able to update a post."""
    #if current user is logged in, get is Id
    current_user = get_jwt_identity() 

    
    print(current_user)
    print(post_id)
    #set to update post content
    title = request.get_json().get('title', '')
    content = request.get_json().get('content', '')
 
    #check if post belongs to current user
    if not current_user:
        return jsonify({
            'status': 'Failed to update post...',
            'message': 'You can only update post you created!'
        }), 401
    #calling update_post method from PostService
    post_updated = update_post(post_id, title, content)
  
    post = get_post_by_Id(post_id)
    return jsonify({
        "message": "Post updated!",
        'post': post
        
    }), 200 
    
  


#Deleting a post
@routes.delete('/post/del/<string:post_id>')
@jwt_required()
def delete(post_id):
    """User must be logged in to be able to delete a post."""
    #if current user is logged in, get is Id
    current_user = get_jwt_identity()


    #check if post belong to current user
    if not current_user:
        return jsonify({
            'status': 'Failed to delete post...',
            'message': 'You can only delete post you created!'
        }), 401
    #we delete and display the user next post
    to_delete = delete_post(post_id, current_user)
    #post = get_by_user_id_and_post_id(post_id, current_user)

    #this will display the next post of the current user
    post = get_by_user_id(current_user)
        
    #if there is no post, inform user they cannot delete other user posts...need to create their own post
    if current_user  and not post:
        return jsonify({
            'status':  'Has no posts!...',
            'message': str(current_user) + ' You cannot delete this post! Click "New Post" button to create your post'
        }), 401
           
    return jsonify({
        'post': post,
        'success': 'Your Post has been deleted!'
    }), 200


"""End implementing methods."""




"""Utils methods."""
#calculate read time of a post
def read_time_post(content):
    #word per minute
    wpm = 225
    # # of words
    numberOfWords = len(content.strip().split())
    readTime = math.ceil(numberOfWords / wpm)
    return readTime


def get_post_state(post_obj):
    if not post_obj:
        posted = False
    
    posted = True
    #post = blog_col.find_one({"posted": posted})
    return posted


#get post read state
@routes.get('/user_posts')
@jwt_required
def get_readtime():
    current_user = get_jwt_identity()

    #empty data list
    data = []

    #get post by current user
    posts = get_by_user_id(current_user)

    #loop through posts
    for post in posts:
        new_data = {
            'title': post.title,
            'content': post.content,
            'author': post.author,
            'readTime': post.readTime
        }
        #add to data list
        data.append(new_data)
    #returning a json object
    return jsonify({'data': data}), 200


"""End utils methods."""