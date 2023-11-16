from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Chat:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO chats (comment, user_id) VALUES (%(comment)s, %(user_id)s);"
        return connectToMySQL("band_schema").query_db(query, data)
    
    @classmethod
    def get_all(cls, data):
        query ="SELECT * FROM chats;"
        return connectToMySQL("band_schema").query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query ="SELECT * FROM chats WHERE id = %(id)s;"
        results = connectToMySQL("band_schema").query_db(query, data)
        return cls(results[0])
    
    @staticmethod
    def validate_chats(chat):
        is_valid = True
        if len(chat['comment']) < 1 :
            flash("Comment must be more then 1 character.")
            is_valid = False
        return is_valid
    
    @classmethod
    def delete_chat(cls, data):
        query ="DELETE FROM chats WHERE id = %(id)s;"
        return connectToMySQL("band_schema").query_db(query, data)
    
    @classmethod
    def update(cls, data, id):
        query = f"UPDATE chats SET comment = %(comment)s WHERE id = {id};"
        return connectToMySQL("band_schema").query_db(query, data)