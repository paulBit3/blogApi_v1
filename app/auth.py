"""Implement basic authentication for our API

This authentication logic will make it easier for Users to be able to sign up, sign in, 
and authenticate their requests to create, update, or delete blog posts.

"""


import datetime
from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from bson import ObjectId
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

#importing swagger sepecification function
#from flasgger import swag_from




import routes


# I used Blueprint to architect our App
auth = Blueprint("auth", __name__, url_prefix="/api/blog/auth")

#user collection. you could also uncomment user_collection. that will create a User collection object in the Db 
#user_collection = routes.user_col

#blog collection.
blog_col = routes.blog_col

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

   


#authentication method
@auth.post('/users/login')
def signin():
    
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
       
        print(username)
        
        # user = user_collection.find_one({'username': username})
        #get the user
        user = get_user(username)

        #hashed password from the database
        print(user)
        #checking if pw from database matches the password the user entered
        is_pass_matching = check_password_hash(user['password'], password)
    
        print(f'Do passwords match? {is_pass_matching}')
        print(is_pass_matching)
        
        if not is_pass_matching:
            error = "Wrong credentials! The password does not match!"
            return jsonify({'error': error}), 401
        else:
            message = "Welcome! " + str(username) + " You are connected!"
            # Then if the password and username are correct we then create access token
            # we also set token to expires in 5 days. So after 5 days the token, user can no longer login with this same token
            #user_id = ObjectId(user_id)
            exp_date = datetime.timedelta(days=5)
            #access = create_access_token(identity=str(user_id), expires_delta=exp_date)
            #refresh = create_refresh_token(identity=str(user_id), expires_delta=exp_date)

            #I used username instead of user_id
            access = create_access_token(identity=str(username), expires_delta=exp_date)
            refresh = create_refresh_token(identity=str(username), expires_delta=exp_date)
            return jsonify({
                'message': message,
                'user': {
                    'access': access,
                    'refresh': refresh,
                    'username': user
                }
                }), 200
    else:
        #return login template if it is a get request
        return render_template('auth/login.html')




#sign out method. we'll use session method to sign user out
@auth.post('/users/logout')
@jwt_required()
def signout():
   #log out the user and redirect to index page
   #session["username"] = None
   session.pop('username', None)
   return jsonify({'message': 'You are logged out! Log back-in to post again!'}), 200


#get a user by username. I pass a param. we could pass ObjectId as well
def get_user(param):
    #u = user_collection.find_one({'username': param})
    u = blog_col.find_one({'username': param})
    if not u:
        return None
    return u

#get a user by Id
def get_user_by_Id(user_id):
    #u = user_collection.find_one({'_id': ObjectId})
    u = blog_col.find_one({'_id': ObjectId(user_id)})
    if not u:
        return None
    return u