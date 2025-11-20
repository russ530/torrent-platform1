from datetime import datetime
from bson import ObjectId

class Torrent:
    @staticmethod
    def create_torrent(db, title, description, size, categories, images, torrent_file_path, uploader_id):
        """Crea un nuovo torrent nel database"""
        torrent_data = {
            'title': title,
            'description': description,
            'size': size,
            'categories': categories,
            'images': images,
            'torrentFilePath': torrent_file_path,
            'uploaderId': ObjectId(uploader_id),
            'createdAt': datetime.utcnow(),
            'downloadCount': 0
        }
        
        result = db.torrents.insert_one(torrent_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_torrents(db, page=1, per_page=20, search=None, category=None, sort_by='createdAt', sort_order='desc'):
        """Recupera torrent con filtri e ordinamento"""
        query = {}
        
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        if category:
            query['categories'] = category
        
        sort_field = sort_by if sort_by in ['createdAt', 'downloadCount', 'size'] else 'createdAt'
        sort_direction = -1 if sort_order == 'desc' else 1
        
        skip = (page - 1) * per_page
        
        torrents = list(db.torrents.find(query)
                       .sort(sort_field, sort_direction)
                       .skip(skip)
                       .limit(per_page))
        
        total = db.torrents.count_documents(query)
        
        # Convert ObjectId to string for JSON serialization
        for torrent in torrents:
            torrent['_id'] = str(torrent['_id'])
            torrent['uploaderId'] = str(torrent['uploaderId'])
        
        return torrents, total
    
    @staticmethod
    def get_torrent_by_id(db, torrent_id):
        """Recupera un torrent per ID"""
        try:
            torrent = db.torrents.find_one({'_id': ObjectId(torrent_id)})
            if torrent:
                torrent['_id'] = str(torrent['_id'])
                torrent['uploaderId'] = str(torrent['uploaderId'])
            return torrent
        except:
            return None
    
    @staticmethod
    def increment_download_count(db, torrent_id):
        """Incrementa il contatore dei download"""
        db.torrents.update_one(
            {'_id': ObjectId(torrent_id)},
            {'$inc': {'downloadCount': 1}}
        )
