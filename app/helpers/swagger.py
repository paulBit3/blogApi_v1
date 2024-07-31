"""
    This module define a sample resource for our swagger api documentation
"""

from flask import Flask, jsonify
from flask_restful import Resource 

class SayHello(Resource):
    def get(self):
        return jsonify({'message': 'Hi there!'})