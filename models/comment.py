from datetime import datetime
from bson import ObjectId

class Comment:
    @staticmethod
    def create_comment(db, torrent_id, user_id, text, rating=0):
        """Crea un nuovo commento nel database"""
        comment_data = {
            'torrentId': ObjectId(torrent_id),
            'userId': ObjectId(user_id),
            'text': text,
            'rating': rating,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        
        result = db.comments.insert_one(comment_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_comments_by_torrent(db, torrent_id):
        """Recupera tutti i commenti di un torrent"""
        comments = list(db.comments.find({'torrentId': ObjectId(torrent_id)})
                           .sort('createdAt', -1))
        
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            comment['userId'] = str(comment['userId'])
            comment['torrentId'] = str(comment['torrentId'])
        
        return comments
