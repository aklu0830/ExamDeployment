from operator import sub

import flask_bcrypt
from flask import flash, session
from decimal import Decimal

from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

dbname = 'paintings'


# model the class after the friend table from our database
class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "select * from paintings;"
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
    def createpainting(self, data):
        query = 'insert into paintings(`name`, `description`, `price`, `created_at`, `updated_at`, `user_id`) values(%(name)s, %(description)s,%(price)s , now(), now(), %(user_id)s);'

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def droppainting(self, data):
        query = "delete from paintings where id=%(painting_id)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return

    @classmethod
    def getpainting(cls, data):
        query = "select * from paintings where id=%(painting_id)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        if len(send) < 1:
            pass
        else:

            return send[0]

    @classmethod
    def updatepainting(cls, data):
        query = "update paintings set `name`=%(name)s, `description`=%(description)s, `price`=%(price)s, `updated_at`=now() where id=%(painting_id)s;"

        send = connectToMySQL(dbname).query_db(query, data)

        return send

    @staticmethod
    def validations(data):
        is_valid = True
        if len(data['name']) < 2:
            flash(u'Name field has to be at least 2 characters', 'painting')
            is_valid = False
        if len(data['description']) < 5:
            flash(u'Description must be at least 5 characters', 'painting')
            is_valid = False
        if Decimal(data['price']) < 1:

            flash(u'Price cannot be less than one', 'painting')
            is_valid = False

        return is_valid
