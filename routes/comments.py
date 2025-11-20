from flask import Blueprint, request, jsonify
from utils.auth import login_required
from datetime import datetime
from bson import ObjectId

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/api/torrents/<torrent_id>/comments', methods=['POST'])
def add_comment(torrent_id):
    @login_required
    def _add_comment():
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({'error': 'Testo del commento richiesto'}), 400
            
            from flask import current_app
            comment_data = {
                'torrentId': ObjectId(torrent_id),
                'userId': ObjectId(request.user_id),
                'text': data['text'],
                'rating': data.get('rating', 0),
                'createdAt': datetime.utcnow(),
                'updatedAt': datetime.utcnow()
            }
            
            result = current_app.db.comments.insert_one(comment_data)
            
            return jsonify({
                'message': 'Commento aggiunto con successo',
                'comment_id': str(result.inserted_id)
            }), 201
            
        except Exception as e:
            return jsonify({'error': f'Errore nell\'aggiunta del commento: {str(e)}'}), 500
    
    return _add_comment()

@comments_bp.route('/api/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    @login_required
    def _update_comment():
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({'error': 'Testo del commento richiesto'}), 400
            
            from flask import current_app
            # Verifica che l'utente sia il proprietario del commento
            comment = current_app.db.comments.find_one({'_id': ObjectId(comment_id)})
            
            if not comment:
                return jsonify({'error': 'Commento non trovato'}), 404
            
            if str(comment['userId']) != request.user_id:
                return jsonify({'error': 'Non autorizzato a modificare questo commento'}), 403
            
            update_data = {
                'text': data['text'],
                'rating': data.get('rating', comment.get('rating', 0)),
                'updatedAt': datetime.utcnow()
            }
            
            current_app.db.comments.update_one(
                {'_id': ObjectId(comment_id)},
                {'$set': update_data}
            )
            
            return jsonify({'message': 'Commento aggiornato con successo'}), 200
            
        except Exception as e:
            return jsonify({'error': f'Errore nell\'aggiornamento del commento: {str(e)}'}), 500
    
    return _update_comment()

@comments_bp.route('/api/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    @login_required
    def _delete_comment():
        try:
            from flask import current_app
            comment = current_app.db.comments.find_one({'_id': ObjectId(comment_id)})
            
            if not comment:
                return jsonify({'error': 'Commento non trovato'}), 404
            
            # L'utente può eliminare solo i propri commenti, tranne admin/moderator
            user = current_app.db.users.find_one({'_id': ObjectId(request.user_id)})
            user_role = user.get('role', 'user') if user else 'user'
            
            can_delete = (str(comment['userId']) == request.user_id or 
                         user_role in ['admin', 'moderator'])
            
            if not can_delete:
                return jsonify({'error': 'Non autorizzato a eliminare questo commento'}), 403
            
            current_app.db.comments.delete_one({'_id': ObjectId(comment_id)})
            
            return jsonify({'message': 'Commento eliminato con successo'}), 200
            
        except Exception as e:
            return jsonify({'error': f'Errore nell\'eliminazione del commento: {str(e)}'}), 500
    
    return _delete_comment()
