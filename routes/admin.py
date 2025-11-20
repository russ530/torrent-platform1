from flask import Blueprint, request, jsonify
from utils.auth import login_required, role_required
from datetime import datetime, timedelta
from bson import ObjectId

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/stats', methods=['GET'])
def get_stats():
    @login_required
    @role_required('admin')
    def _get_stats():
        try:
            from flask import current_app
            # Statistiche generali
            total_users = current_app.db.users.count_documents({})
            total_torrents = current_app.db.torrents.count_documents({})
            total_downloads = current_app.db.downloads.count_documents({})
            total_comments = current_app.db.comments.count_documents({})
            
            # Torrent più popolari (per download count)
            popular_torrents = list(current_app.db.torrents.find()
                                   .sort('downloadCount', -1)
                                   .limit(10))
            
            for torrent in popular_torrents:
                torrent['_id'] = str(torrent['_id'])
                torrent['uploaderId'] = str(torrent['uploaderId'])
            
            # Categorie più popolari
            pipeline = [
                {'$unwind': '$categories'},
                {'$group': {'_id': '$categories', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
            ]
            popular_categories = list(current_app.db.torrents.aggregate(pipeline))
            
            # Nuovi torrent (ultimi 7 giorni)
            week_ago = datetime.utcnow() - timedelta(days=7)
            new_torrents = current_app.db.torrents.count_documents({
                'createdAt': {'$gte': week_ago}
            })
            
            # Utenti attivi (ultimi 7 giorni)
            active_users = len(current_app.db.downloads.distinct('userId', {
                'downloadedAt': {'$gte': week_ago}
            }))
            
            return jsonify({
                'stats': {
                    'total_users': total_users,
                    'total_torrents': total_torrents,
                    'total_downloads': total_downloads,
                    'total_comments': total_comments,
                    'new_torrents_week': new_torrents,
                    'active_users_week': active_users
                },
                'popular_torrents': popular_torrents,
                'popular_categories': popular_categories
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Errore nel recupero delle statistiche: {str(e)}'}), 500
    
    return _get_stats()

@admin_bp.route('/api/admin/users', methods=['GET'])
def get_users():
    @login_required
    @role_required('admin')
    def _get_users():
        try:
            from flask import current_app
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 20))
            
            skip = (page - 1) * per_page
            users = list(current_app.db.users.find()
                        .skip(skip)
                        .limit(per_page))
            
            total = current_app.db.users.count_documents({})
            
            # Convert ObjectId to string and remove password hash
            for user in users:
                user['_id'] = str(user['_id'])
                user.pop('passwordHash', None)
            
            return jsonify({
                'users': users,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Errore nel recupero degli utenti: {str(e)}'}), 500
    
    return _get_users()

@admin_bp.route('/api/admin/users/<user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    @login_required
    @role_required('admin')
    def _update_user_role():
        try:
            data = request.get_json()
            
            if not data or 'role' not in data:
                return jsonify({'error': 'Ruolo richiesto'}), 400
            
            from models.user import User
            from flask import current_app
            success = User.update_role(current_app.db, user_id, data['role'])
            
            if not success:
                return jsonify({'error': 'Errore nell\'aggiornamento del ruolo'}), 400
            
            return jsonify({'message': 'Ruolo aggiornato con successo'}), 200
            
        except Exception as e:
            return jsonify({'error': f'Errore nell\'aggiornamento del ruolo: {str(e)}'}), 500
    
    return _update_user_role()

@admin_bp.route('/api/admin/users/<user_id>/ban', methods=['PUT'])
def toggle_ban_user(user_id):
    @login_required
    @role_required('admin')
    def _toggle_ban_user():
        try:
            data = request.get_json()
            
            if not data or 'banned' not in data:
                return jsonify({'error': 'Stato ban richiesto'}), 400
            
            from flask import current_app
            result = current_app.db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'banned': data['banned']}}
            )
            
            if result.modified_count == 0:
                return jsonify({'error': 'Utente non trovato'}), 404
            
            action = "bannato" if data['banned'] else "sbannato"
            return jsonify({'message': f'Utente {action} con successo'}), 200
            
        except Exception as e:
            return jsonify({'error': f'Errore nel ban utente: {str(e)}'}), 500
    
    return _toggle_ban_user()
