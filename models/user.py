from datetime import datetime
import bcrypt
from bson import ObjectId

class User:
    ROLES = ['guest', 'user', 'moderator', 'admin']
    
    @staticmethod
    def create_user(db, username, email, password, role='user'):
        """Crea un nuovo utente nel database"""
        if db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            return None, "Username o email già esistenti"
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            'username': username,
            'email': email,
            'passwordHash': password_hash.decode('utf-8'),
            'role': role,
            'banned': False,
            'createdAt': datetime.utcnow()
        }
        
        result = db.users.insert_one(user_data)
        return str(result.inserted_id), None
    
    @staticmethod
    def verify_password(db, email, password):
        """Verifica la password dell'utente"""
        user = db.users.find_one({'email': email, 'banned': False})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['passwordHash'].encode('utf-8')):
            return user
        return None
    
    @staticmethod
    def get_user_by_id(db, user_id):
        """Recupera un utente per ID"""
        try:
            return db.users.find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    @staticmethod
    def update_role(db, user_id, new_role):
        """Aggiorna il ruolo di un utente"""
        if new_role not in User.ROLES:
            return False
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'role': new_role}}
        )
        return result.modified_count > 0
