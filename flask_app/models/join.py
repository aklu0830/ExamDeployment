from operator import sub

import flask_bcrypt
from flask import flash, session

from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

dbname = 'paintings'


# model the class after the friend table from our database
class Join:
    def __init__(self, data):
        self.user_user_id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.users_created_at = data['created_at']
        self.users_updated_at = data['updated_at']
        self.painting_id = data['paintings.id']
        self.painting_name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.painting_created_at = data['paintings.created_at']
        self.painting_updated_at = data['paintings.updated_at']
        self.painting_user_id = data['user_id']

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "select *, paintings.* from users JOIN paintings ON users.id = paintings.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(dbname).query_db(query)
        # Create an empty list to append our instances of friends
        userlist = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            userlist.append(cls(user))
            print(user)
        return userlist

    @classmethod
    def getPainting(cls, data):
        query = "select *, paintings.* from users JOIN paintings ON users.id = paintings.user_id where paintings.id=%(painting_id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        send = connectToMySQL(dbname).query_db(query, data)

        userlist = []
        # Iterate over the db results and create instances of friends with cls.
        for user in send:
            userlist.append(cls(user))
            print(user)
        return userlist
