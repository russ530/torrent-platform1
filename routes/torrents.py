from flask import Blueprint, request, jsonify, send_file
import os
from models.torrent import Torrent
from models.user import User
from utils.auth import login_required, role_required
from datetime import datetime
from bson import ObjectId

torrents_bp = Blueprint('torrents', __name__)

@torrents_bp.route('/api/torrents', methods=['GET'])
def get_torrents():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        search = request.args.get('search')
        category = request.args.get('category')
        sort_by = request.args.get('sort_by', 'createdAt')
        sort_order = request.args.get('sort_order', 'desc')
        
        from flask import current_app
        torrents, total = Torrent.get_torrents(
            current_app.db, page, per_page, search, category, sort_by, sort_order
        )
        
        # Recupera informazioni sull'uploader per ogni torrent
        for torrent in torrents:
            uploader = User.get_user_by_id(current_app.db, torrent['uploaderId'])
            torrent['uploaderUsername'] = uploader['username'] if uploader else 'Unknown'
            if 'createdAt' in torrent and hasattr(torrent['createdAt'], 'isoformat'):
                torrent['createdAt'] = torrent['createdAt'].isoformat()
        
        return jsonify({
            'torrents': torrents,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Errore nel recupero dei torrent: {str(e)}'}), 500

@torrents_bp.route('/api/torrents/<torrent_id>', methods=['GET'])
def get_torrent(torrent_id):
    try:
        from flask import current_app
        torrent = Torrent.get_torrent_by_id(current_app.db, torrent_id)
        
        if not torrent:
            return jsonify({'error': 'Torrent non trovato'}), 404
        
        # Recupera informazioni sull'uploader
        uploader = User.get_user_by_id(current_app.db, torrent['uploaderId'])
        torrent['uploaderUsername'] = uploader['username'] if uploader else 'Unknown'
        
        # Recupera commenti
        comments = list(current_app.db.comments.find({'torrentId': ObjectId(torrent_id)})
                           .sort('createdAt', -1))
        
        for comment in comments:
            comment_user = User.get_user_by_id(current_app.db, comment['userId'])
            comment['userUsername'] = comment_user['username'] if comment_user else 'Unknown'
            comment['_id'] = str(comment['_id'])
            comment['userId'] = str(comment['userId'])
            comment['torrentId'] = str(comment['torrentId'])
            if 'createdAt' in comment and hasattr(comment['createdAt'], 'isoformat'):
                comment['createdAt'] = comment['createdAt'].isoformat()
        
        torrent['comments'] = comments
        
        if 'createdAt' in torrent and hasattr(torrent['createdAt'], 'isoformat'):
            torrent['createdAt'] = torrent['createdAt'].isoformat()
        
        return jsonify({'torrent': torrent}), 200
        
    except Exception as e:
        return jsonify({'error': f'Errore nel recupero del torrent: {str(e)}'}), 500

@torrents_bp.route('/api/torrents', methods=['POST'])
def upload_torrent():
    @login_required
    @role_required('user')
    def _upload_torrent():
        try:
            data = request.get_json()
            
            if not data or not all(k in data for k in ['title', 'description', 'size', 'categories']):
                return jsonify({'error': 'Dati mancanti'}), 400
            
            from flask import current_app
            # In un'implementazione reale, qui gestiresti l'upload del file .torrent
            torrent_file_path = f"torrents/{datetime.utcnow().timestamp()}.torrent"
            
            torrent_id = Torrent.create_torrent(
                current_app.db,
                data['title'],
                data['description'],
                data['size'],
                data['categories'],
                data.get('images', []),
                torrent_file_path,
                request.user_id
            )
            
            return jsonify({
                'message': 'Torrent caricato con successo',
                'torrent_id': torrent_id
            }), 201
            
        except Exception as e:
            return jsonify({'error': f'Errore nel caricamento del torrent: {str(e)}'}), 500
    
    return _upload_torrent()

@torrents_bp.route('/api/torrents/<torrent_id>/download', methods=['POST'])
def download_torrent(torrent_id):
    @login_required
    def _download_torrent():
        try:
            from flask import current_app
            torrent = Torrent.get_torrent_by_id(current_app.db, torrent_id)
            
            if not torrent:
                return jsonify({'error': 'Torrent non trovato'}), 404
            
            # Registra il download
            download_data = {
                'torrentId': ObjectId(torrent_id),
                'userId': ObjectId(request.user_id),
                'downloadedAt': datetime.utcnow()
            }
            current_app.db.downloads.insert_one(download_data)
            
            # Incrementa il contatore dei download
            Torrent.increment_download_count(current_app.db, torrent_id)
            
            # In un'implementazione reale, qui restituiresti il file .torrent
            return jsonify({
                'message': 'Download registrato con successo',
                'torrent_file': torrent['torrentFilePath']
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Errore durante il download: {str(e)}'}), 500
    
    return _download_torrent()
