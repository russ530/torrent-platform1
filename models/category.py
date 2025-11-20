from datetime import datetime
from bson import ObjectId

class Category:
    @staticmethod
    def create_category(db, name, description):
        """Crea una nuova categoria"""
        category_data = {
            'name': name,
            'description': description,
            'createdAt': datetime.utcnow()
        }
        
        result = db.categories.insert_one(category_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all_categories(db):
        """Recupera tutte le categorie"""
        categories = list(db.categories.find())
        
        for category in categories:
            category['_id'] = str(category['_id'])
        
        return categories
    
    @staticmethod
    def get_category_by_name(db, name):
        """Recupera una categoria per nome"""
        category = db.categories.find_one({'name': name})
        
        if category:
            category['_id'] = str(category['_id'])
        
        return category
