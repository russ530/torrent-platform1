from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # MongoDB Connection
    try:
        client = MongoClient(app.config['MONGO_URI'])
        app.db = client[app.config['DATABASE_NAME']]
        print("✅ Connesso a MongoDB Atlas con successo!")
    except Exception as e:
        print(f"❌ Errore di connessione a MongoDB: {e}")
        return None
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Store db in request context
    @app.before_request
    def before_request():
        request.app = app
    
    # Register Blueprints
    from routes.auth import auth_bp
    from routes.torrents import torrents_bp
    from routes.comments import comments_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(torrents_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(admin_bp)
    
    # Main route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/register')
    def register():
        return render_template('register.html')
    
    @app.route('/upload')
    def upload():
        return render_template('upload.html')
    
    @app.route('/profile')
    def profile():
        return render_template('profile.html')
    
    @app.route('/admin')
    def admin():
        return render_template('admin.html')
    
    @app.route('/torrent/<torrent_id>')
    def torrent_detail(torrent_id):
        return render_template('torrent_detail.html')
    
    # Health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'database': 'connected'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    if app:
        app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
