🤔About the Project:
------
    
    A simple CRUD BlogAPI project. 
    BlogAPI allows users to perform CRUD operations such as 
    creating, listing, updating and deleting blog posts. 
----

- Back-end techs stack: Python/Flask and MongoDB, and Swagger for the API documentation
    
------  
Satisfied these requirements:
---
- User login or Create an account to login
- User Create, Update, View, and  Delete a blog post
- User Logout from their account
- APP display blog post created by user
- User can see blogs post on an index html page as well by navigating to  http://127.0.0.1:8000
- The API is tested using Postman and AdcvancedAPI tool
- The API is Documented and tested using Swagger

You can download it to your local or clone it  ```git clone: https://github.com/paulBit3/blogApi_v1.git```

------

--- Install Dependencies for the project:

python3 -m pip install -r requirements.txt
or 
pip install -r requirements.txt


To run or start the app, Navigate to the /app folder to the command line on Windows or Terminal on Mac, or Terminal in VS Studio Code and  type

--- python ./run.py
or
--- python run.py

------ API Endpoints
For the API endpoints documentation, Navigate to
http://127.0.0.1:8000/api/docs/#/


After creating a post, it displays on the index page.
In your browser, Navigate to http://127.0.0.1:8000

- Authentication Endpoint URI

1- Signup
   http://127.0.0.1:8000/api/blog/auth/users/signup

2- Signin
   http://127.0.0.1:8000/api/blog/auth/users/login

3- Sign out or logout
   http://127.0.0.1:8000/api/blog/auth/users/logout


- Blog Endpoint URI

1- Create new post
   http://127.0.0.1:8000/api/blog/post


2- Get a single post(post Id here just shows you where to type it in the link. Please remove it and enter your new post Id)
   http://127.0.0.1:8000/api/blog/post/66a149df116ba7b281d41a67


3- Get all posts
   http://127.0.0.1:8000/api/blog/posts/


4- Modifying or Editing a post(post Id here just shows you where to type it in the link to perform EDITING. remove it and enter your new post Id )
   http://127.0.0.1:8000/api/blog/post/66a149df116ba7b281d41a67/edit


5- Delete a post(post Id here is just to show you where to type the Id in the link)
   http://127.0.0.1:8000/api/blog/post/del/66a149df116ba7b281d41a67
   
--------
---- Demo
--
A complete project live demo is here: [Complete Demo on postman](https://gemoo.com/tools/upload-video/share/676539270156771328?codeId=PYL3aw7BYgQZK&card=676539267866681344)

A complete demo on Swagger is here: [Complete Demo on Swagger](https://gemoo.com/tools/upload-video/share/677388842189967360?codeId=DGYyn6rz6YKdY&card=677388839774048256)

------------

Code snipet-------

BlogPost Service code snipet
```Python

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

```
User registration code snipet
```Python
error = None

#register method

@auth.post('/users/signup')
def signup():
    if request.method == 'POST':
        body = request.get_json()

        #getting username  and password sent by the user from the JSON
        pw = body.get('password')
        hash_password = generate_password_hash(pw)

        user = {
           'username' : body.get('username'),
           'password': hash_password
        }
      
        #check if username or password is empty
        if not body.get('username'):
            error = "You must enter a Username. This field is required!"
            return jsonify({'error': error}), 400
        elif not body.get('password'):
            error = "You must enter a Password. This field is required!"
            return jsonify({'error': error}), 400
        elif get_user(body.get('username')) :
            #print(user.username)
            error = "The username " + str(body.get('username')) + ", already exist!"
            return jsonify({'error': error}), 409
        else:
        
            #pass the data to our USer class and save it to database
            #data = User(username = username, password = pw)
            #insert_data = user_collection.insert_one(user)

            insert_data = blog_col.insert_one(user)
            return jsonify({
                'message': "your account is successfully created!",
                'user': {
                    
                    'data': user
                    }
            }), 201
    else:
        #retern signup template if it is a get request
        return render_template('auth/signup.html')

   ```

--Screenshots for showcase purposes

<img width="919" alt="Swagger_screen_2024-07-31 114136" src="https://github.com/user-attachments/assets/de874a1a-6bc1-4efe-8d77-b7e9b8f82f88">
<img width="922" alt="Swagger_screen_2024-07-31 114031" src="https://github.com/user-attachments/assets/5eb8af30-4e83-43c3-b293-b5bd8ee024e4">
<img width="926" alt="Swagger_screen_2024-07-31 003350" src="https://github.com/user-attachments/assets/18bfde11-6d03-4fdc-826d-689f9730400c">
<img width="908" alt="Swagger_screen_2024-07-29 211020" src="https://github.com/user-attachments/assets/7aae6447-8769-419b-aed8-5259fd32388a">
<img width="944" alt="Swagger_screen_2024-07-29 184750" src="https://github.com/user-attachments/assets/f922263b-4a01-469e-ab54-6c126343eff4">
<img width="925" alt="Swagger_screen_2024-07-29 085547" src="https://github.com/user-attachments/assets/91fd9a9b-343a-4b55-a54d-3f7ef52e65eb">
![Swagger_screen_2024-07-29 085506](https://github.com/user-attachments/assets/bb0c2d6c-81a7-4577-9f05-a896c95637b7)
<img width="913" alt="Swagger_screen_2024-07-29 080429" src="https://github.com/user-attachments/assets/1fbecfb0-3fb0-42a3-82ad-196845b68f84">
![Screenshot 2024-07-24 095333](https://github.com/user-attachments/assets/42f472e2-d1b9-4293-9469-4042b4e499c2)
<img width="635" alt="Screenshot 2024-07-24 095038" src="https://github.com/user-attachments/assets/532231b3-6aa7-469d-9473-5953b67df9f0">
<img width="635" alt="Screenshot 2024-07-24 094421" src="https://github.com/user-attachments/assets/27a4ae28-df6a-40d0-a6f8-f22bd6da9d90">
![Screenshot 2024-07-24 094357](https://github.com/user-attachments/assets/bd2b5f9f-9b14-4b80-a2e6-a0dd540168ad)
<img width="635" alt="Screenshot 2024-07-24 094255" src="https://github.com/user-attachments/assets/08ffb955-39fd-4dd4-97ff-9a3846def5f7">
<img width="660" alt="Screenshot 2024-07-23 225122" src="https://github.com/user-attachments/assets/074057d3-9857-4378-8d49-f79336ad6169">
<img width="838" alt="Screenshot 2024-07-23 190619" src="https://github.com/user-attachments/assets/eef780c7-5daf-4e4d-bd8b-777962f2504b">
![Screenshot 2024-07-22 210125](https://github.com/user-attachments/assets/6bc88612-9b0b-46ba-a55c-6aaf670c58b7)
<img width="936" alt="blog_api_index_2_2024-07-31 160926" src="https://github.com/user-attachments/assets/15335f3f-024d-4312-bced-0afc55e454f6">
<img width="975" alt="blog_api_index_1_2024-07-31 160814" src="https://github.com/user-attachments/assets/4f319954-97bb-40ad-8d3b-0dbc8d21febe">

