"""
blogAPI - A blog API for user to make CRUP operation.

"""
import json
import os
from flask import Flask, jsonify, redirect, url_for, render_template
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS



from database import db_init
from database.db_init import db_initializer

#import MONGO URI
from database.models import Post
from database.uri import URI

#imported our config class
from helpers.config import Config

#getting our swagger sample
from helpers.swagger import SayHello

#import authentication module
from auth import auth

#import routes(where we have blog post implementation) module
from routes import retrieve_all_post, routes

#import our JSON Encoder class
from helpers.MyCustomJsonEncoder import MongoDbJSONEncoder, ObjectIdConverter

#serve to populate index blog post page
from services.PostService import list_posts





def create_app(test_config = None):
    #a new Flask application instance
    app = Flask(__name__, instance_relative_config=True)
    

    #json ending our app
    app.json_encoder = MongoDbJSONEncoder
    app.url_map.converters['objectid'] = ObjectIdConverter
    #print(Config.JWT_SECRET_KEY) to see if we got the Jwt secret key

    #setting authorization
   

   

    #register our modules

    #blueprint for auth routes
    app.register_blueprint(auth)

    #blueprint for no-auth routes(post, and others)
    app.register_blueprint(routes)
   

    if test_config:
               
        app.config.from_mapping(
            #passing our config class object
            app.config.from_object(Config.SECRET_KEY),
            app.config.from_object(Config.JWT_SECRET_KEY),
            URI,
            
        SWAGGER={
            'title': "Blog API",
            'uiversion': 3
        }
            
        )
    else:
        app.config.from_mapping(test_config)
    


    app.config.from_object(Config),
    app.config.from_object(Config)
 
    #app.config.from_envvar(Config.JWT_SECRET_KEY)
  
    #configure swagger ++++

    #url for exposing Swagger UI
    SWAGGER_URL= '/api/docs'

    #our API url for Swagger
    API_URL = '/swagger1.json'
    
    #create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Blog API"
        }
    )
    #register swagger blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/swagger1.json')
    def swagger():
        with open('swagger1.json', 'r') as f:
            return jsonify(json.load(f))

    #end swagger configuration +++
    

    #db initialize
    db_init.app = app
    db_initializer(app)


    #encrypting our app
    #bcrypt = Bcrypt(app)


    #initialize JWT
    JWTManager(app)




    #main view function to display blog posts on index page when our blog website is visted
    @app.get('/')
    def home():
        #return "Hello!"
        posts_data = list_posts()
        posts = [Post.post_instance(post) for post in posts_data]
        return render_template("index.html", posts=posts)

    CORS(app)

    

    #set the ap to run on localhost and port 5000
    app.run(host="127.0.0.1", port=8000, debug=True)

    #export the app
    return app


        







