
from flask_mongoengine import MongoEngine




#mongo engine instance
db = MongoEngine()



#initializing our database by passing app as parameter
def db_initializer(app):
    db.init_app(app)

