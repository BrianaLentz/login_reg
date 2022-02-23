from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL('login_reg').query_db(query, data)

    @staticmethod
    def validate_reg(user):
        print(user)
        is_valid = True
        if not user['first_name'].isalpha():
            flash("Letters only", 'reg')
            is_valid = False
        if len(user['first_name']) <2:
            flash("Name must be atleast 2 characters.", 'reg')
            is_valid = False
        if not user['last_name'].isalpha():
            flash("Letters only", 'reg')
            is_valid = False
        if len(user['last_name']) <2:
            flash("Name must be atleast 2 characters.", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address', 'reg')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long.', 'reg')
            is_valid = False
        if user['password'] != (user['password_confirm']):
            flash('Password does not match', 'reg')
            is_valid = False
        return is_valid

    @classmethod
    def validate_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_reg').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

