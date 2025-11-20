from flask import Blueprint, request, jsonify
from models.user import User
from utils.auth import generate_token
from utils.validators import validate_email, validate_username, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Dati mancanti'}), 400
        
        # Validazione
        if not validate_username(data['username']):
            return jsonify({'error': 'Username non valido (3-50 caratteri, solo lettere, numeri, _ e -)'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'error': 'Email non valida'}), 400
        
        if not validate_password(data['password']):
            return jsonify({'error': 'Password non valida (minimo 8 caratteri, almeno una maiuscola, una minuscola e un numero)'}), 400
        
        from flask import current_app
        user_id, error = User.create_user(
            current_app.db,
            data['username'],
            data['email'],
            data['password']
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Registrazione completata con successo',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Errore durante la registrazione: {str(e)}'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Email e password richieste'}), 400
        
        from flask import current_app
        user = User.verify_password(current_app.db, data['email'], data['password'])
        
        if not user:
            return jsonify({'error': 'Credenziali non valide'}), 401
        
        token = generate_token(str(user['_id']), user['role'])
        
        return jsonify({
            'message': 'Login effettuato con successo',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Errore durante il login: {str(e)}'}), 500

@auth_bp.route('/api/profile', methods=['GET'])
def get_profile():
    from utils.auth import login_required
    
    @login_required
    def _get_profile():
        try:
            from flask import current_app
            user = User.get_user_by_id(current_app.db, request.user_id)
            
            if not user:
                return jsonify({'error': 'Utente non trovato'}), 404
            
            return jsonify({
                'user': {
                    'id': str(user['_id']),
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'createdAt': user['createdAt'].isoformat() if hasattr(user['createdAt'], 'isoformat') else str(user['createdAt'])
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Errore nel recupero del profilo: {str(e)}'}), 500
    
    return _get_profile()
