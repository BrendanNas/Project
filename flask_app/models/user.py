from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.chat import Chat
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chats = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("band_schema").query_db(query, data)
    
    @classmethod
    def get_by_email(cls, data):
        query ="SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("band_schema").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN chats ON users.id = chats.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL("band_schema").query_db(query, data)
        user = cls(results[0])
        for row in results:
            chat_data = {
                "id": row["chats.id"],
                "comment": row["comment"],
                "created_at": row["chats.created_at"],
                "updated_at": row["chats.updated_at"],
                "user_id": row["id"]
            }
            user.chats.append(Chat(chat_data))
        return user
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be more then 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be more then 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email.")
            is_valid = False
        if len(user['password']) < 5:
            flash("Password must be more then 5 characters.")
            is_valid = False
        if user['password'] != user['c_password']:
            flash("Passwords don't match.")
            is_valid = False
        return is_valid