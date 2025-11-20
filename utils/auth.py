import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from config import Config

def generate_token(user_id, role):
    """Genera un token JWT"""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

def verify_token(token):
    """Verifica un token JWT"""
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    """Decorator per richiedere l'autenticazione"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Token mancante o malformato'}), 401
        
        token = token.split(' ')[1]
        payload = verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Token non valido o scaduto'}), 401
        
        request.user_id = payload['user_id']
        request.user_role = payload['role']
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """Decorator per controllare i ruoli"""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_role = getattr(request, 'user_role', 'guest')
            roles_hierarchy = ['guest', 'user', 'moderator', 'admin']
            
            if roles_hierarchy.index(user_role) < roles_hierarchy.index(required_role):
                return jsonify({'error': 'Permessi insufficienti'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
