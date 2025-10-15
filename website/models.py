from flask import current_app
from datetime import datetime

class MessageModel:
    """Handles MongoDB operations for contact messages."""

    @staticmethod
    def insert_message(name, email, message, subject=None):
        messages_collection = current_app.mongo_db.messages
        messages_collection.insert_one({
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "date": datetime.utcnow()
        })

    @staticmethod
    def get_all_messages():
        messages_collection = current_app.mongo_db.messages
        return list(messages_collection.find().sort("date", -1))

    @staticmethod
    def get_message_by_email(email):
        messages_collection = current_app.mongo_db.messages
        return messages_collection.find_one({"email": email})
