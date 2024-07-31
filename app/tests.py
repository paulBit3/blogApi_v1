"""
    Basic tests for our Post model. 
    This class serves to ensure that a logged-in user can create a blog post with a title and content
"""

#importing unit test 
from unittest import TestCase
from unittest.mock import patch

#importing mongo mock
from mongomock import MongoClient

#importing create app method
from app import create_app

#import app initializer
from database.db_init import db_initializer

#importing DB Uri
from database.uri import URI



#db uri
db_uri = URI.MONGO_DB_URI
client = MongoClient(db_uri)

#connecting to the database
db = client.get_database('Blog')

#preparing collection for our test
blog_col = db.get_collection('blogData')

class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()

class TestBlogPosts(TestCase):
    #method to create a blog posts
    def test_create_blog_post(self):
        request = {
            "title": "Stock",
            "author": "ValueGlance",
            "content": "Stock market is so stable today with AI. ValueGlance provides you a best blueprint to assist youin your stock investment path!"
        }

        with patch.object(db_uri, PyMongoMock()):
            app = create_app(db).test_client()
            response = app.post("api/blog/post", json=request)
            self.assertEqual(response.status_code, 201)

            # Validate the content
            response_json = response.get_json()
            expected_json = {
                "_id": response_json["_id"],
                "title": "Stock",
                "author": "ValueGlance",
                "content": "Stock market is so stable today with AI. ValueGlance provides you a best blueprint to assist youin your stock investment path!",
                "posted": True,
                "readTime": 1
            }
            self.assertEqual(response_json, expected_json)