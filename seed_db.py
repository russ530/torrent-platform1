#!/usr/bin/env python
"""
Script per eliminare dati presenti nel database e popolarlo con nuovi dati
Uso: python seed_db.py
"""

from pymongo import MongoClient
from config import Config
from models.user import User
from models.torrent import Torrent
from datetime import datetime, timedelta
import random

# Connessione al database
client = MongoClient(Config.MONGO_URI)
db = client[Config.DATABASE_NAME]

# Ottieni tutte le collezioni
print("🗑️  Eliminazione di tutti i dati presenti nel database...")
collections = db.list_collection_names()

for collection in collections:
    deleted = db[collection].delete_many({})
    print(f"  ✅ Eliminati {deleted.deleted_count} documenti da '{collection}'")

print("✅ Database ripulito da tutti i dati!\n")

# Crea utenti di test
print("👥 Creazione utenti di test...")
test_users = [
    ('admin_user', 'admin@torrent.com', 'Admin123456', 'admin'),
    ('moderator_user', 'moderator@torrent.com', 'Moderator123456', 'moderator'),
    ('alice', 'alice@torrent.com', 'Alice123456', 'user'),
    ('bob', 'bob@torrent.com', 'Bob123456', 'user'),
    ('charlie', 'charlie@torrent.com', 'Charlie123456', 'user'),
    ('diana', 'diana@torrent.com', 'Diana123456', 'user'),
    ('eve', 'eve@torrent.com', 'Eve123456', 'user'),
    ('frank', 'frank@torrent.com', 'Frank123456', 'user'),
]

user_ids = {}
for username, email, password, role in test_users:
    user_id, error = User.create_user(db, username, email, password, role)
    if error:
        print(f"  ❌ Errore nella creazione di {username}: {error}")
    else:
        user_ids[username] = user_id
        print(f"  ✅ Utente {username} creato (Ruolo: {role})")

print()

# Dati per i torrent di test
torrent_data = [
    # Film
    {
        'title': 'The Matrix (1999)',
        'description': 'Un hacker scopre la vera natura della sua realtà e il suo ruolo nel conflitto globale.',
        'size': 2048,
        'categories': ['Film', 'Azione', '1999'],
        'images': ['https://via.placeholder.com/300x400?text=Matrix'],
        'uploader': 'alice'
    },
    {
        'title': 'Inception (2010)',
        'description': 'Un ladro che ruba i segreti aziendali tramite la tecnologia dei sogni.',
        'size': 2560,
        'categories': ['Film', 'Fantascienza', '2010'],
        'images': ['https://via.placeholder.com/300x400?text=Inception'],
        'uploader': 'bob'
    },
    {
        'title': 'The Dark Knight (2008)',
        'description': 'Batman affronta il Joker, un criminale carismatico che vuole gettare Gotham nel caos.',
        'size': 2750,
        'categories': ['Film', 'Azione', 'Thriller'],
        'images': ['https://via.placeholder.com/300x400?text=DarkKnight'],
        'uploader': 'charlie'
    },
    # Serie TV
    {
        'title': 'Breaking Bad - Stagione 1',
        'description': 'Un insegnante di chimica si trasforma in criminale per proteggere la sua famiglia.',
        'size': 5120,
        'categories': ['Serie TV', 'Drama', 'Crime'],
        'images': ['https://via.placeholder.com/300x400?text=BreakingBad'],
        'uploader': 'diana'
    },
    {
        'title': 'Game of Thrones - Stagione 1',
        'description': 'Una saga epica di potere, intrighi e draghi nel mondo di Westeros.',
        'size': 6144,
        'categories': ['Serie TV', 'Fantasy', 'Drama'],
        'images': ['https://via.placeholder.com/300x400?text=GameOfThrones'],
        'uploader': 'eve'
    },
    # Musica
    {
        'title': 'Pink Floyd - The Wall (Album Completo)',
        'description': 'Album rock progressivo del 1979 con tutta la discografia e bonus tracks.',
        'size': 512,
        'categories': ['Musica', 'Rock', 'Classico'],
        'images': ['https://via.placeholder.com/300x400?text=TheWall'],
        'uploader': 'frank'
    },
    {
        'title': 'The Beatles - Abbey Road (Remastered)',
        'description': 'L\'ultimo album registrato dei Beatles in versione rimasterizzata 2024.',
        'size': 450,
        'categories': ['Musica', 'Pop', 'Rock'],
        'images': ['https://via.placeholder.com/300x400?text=AbbeyRoad'],
        'uploader': 'alice'
    },
    # Giochi
    {
        'title': 'The Witcher 3 - Wild Hunt',
        'description': 'RPG open-world con Geralt di Rivia alla ricerca di sua figlia.',
        'size': 51200,
        'categories': ['Giochi', 'RPG', 'Avventura'],
        'images': ['https://via.placeholder.com/300x400?text=Witcher3'],
        'uploader': 'bob'
    },
    {
        'title': 'Cyberpunk 2077',
        'description': 'Gioco di ruolo futuristico ambientato in una metropoli hi-tech.',
        'size': 102400,
        'categories': ['Giochi', 'Azione', 'RPG'],
        'images': ['https://via.placeholder.com/300x400?text=Cyberpunk'],
        'uploader': 'charlie'
    },
    # Software
    {
        'title': 'Blender 4.0 - 3D Modeling Suite',
        'description': 'Suite completa per modellazione 3D, animazione e rendering.',
        'size': 256,
        'categories': ['Software', 'Grafica', 'Design'],
        'images': ['https://via.placeholder.com/300x400?text=Blender'],
        'uploader': 'diana'
    },
    {
        'title': 'Adobe Creative Cloud 2024',
        'description': 'Suite completa Adobe con Photoshop, Illustrator, Premiere Pro e altro.',
        'size': 512,
        'categories': ['Software', 'Grafica', 'Multimedia'],
        'images': ['https://via.placeholder.com/300x400?text=AdobeCC'],
        'uploader': 'eve'
    },
    # Libri
    {
        'title': 'Dune - Frank Herbert',
        'description': 'Capolavoro della fantascienza su un pianeta deserto e il suo popolo.',
        'size': 5,
        'categories': ['Libri', 'Fantascienza', 'Classico'],
        'images': ['https://via.placeholder.com/300x400?text=Dune'],
        'uploader': 'frank'
    },
    {
        'title': 'Harry Potter - Serie Completa',
        'description': 'I sette libri della celebre saga del giovane mago di Hogwarts.',
        'size': 15,
        'categories': ['Libri', 'Fantasy', 'Young Adult'],
        'images': ['https://via.placeholder.com/300x400?text=HarryPotter'],
        'uploader': 'alice'
    },
]

# Crea i torrent
print("🎬 Creazione torrent di test...")
torrent_ids = []
for i, data in enumerate(torrent_data):
    uploader_id = user_ids[data['uploader']]
    
    # Crea il torrent
    torrent_id = Torrent.create_torrent(
        db,
        data['title'],
        data['description'],
        data['size'],
        data['categories'],
        data['images'],
        f"torrents/{datetime.utcnow().timestamp()}.torrent",
        uploader_id
    )
    
    torrent_ids.append(torrent_id)
    
    # Aggiungi download casuali
    download_count = random.randint(5, 500)
    db.torrents.update_one(
        {'_id': __import__('bson').ObjectId(torrent_id)},
        {'$set': {'downloadCount': download_count}}
    )
    
    print(f"  ✅ Torrent '{data['title']}' creato ({download_count} download)")

print()

# Crea commenti
print("💬 Creazione commenti di test...")
comments_count = 0
for torrent_id in torrent_ids:
    num_comments = random.randint(0, 5)
    for _ in range(num_comments):
        user_idx = random.randint(0, len(test_users) - 1)
        commenter_id = list(user_ids.values())[user_idx]
        
        comments = [
            "Ottimo torrent, veloce e pulito!",
            "Consigliato a tutti!",
            "Funziona perfettamente.",
            "Qualità eccellente!",
            "Grazie per la condivisione.",
            "Download velocissimo!",
            "Molto soddisfatto!",
            "5/5 stelle!",
            "Perfetto per le mie esigenze.",
            "Merita tutto il supporto!",
        ]
        
        comment_text = random.choice(comments)
        rating = random.randint(3, 5)
        
        comment_data = {
            'torrentId': __import__('bson').ObjectId(torrent_id),
            'userId': __import__('bson').ObjectId(commenter_id),
            'text': comment_text,
            'rating': rating,
            'createdAt': datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            'updatedAt': datetime.utcnow() - timedelta(days=random.randint(0, 30))
        }
        
        db.comments.insert_one(comment_data)
        comments_count += 1

print(f"  ✅ Creati {comments_count} commenti\n")

# Statitiche finali
print("=" * 50)
print("📊 STATISTICHE FINALI")
print("=" * 50)
print(f"✅ Utenti creati: {len(test_users)}")
print(f"✅ Torrent creati: {len(torrent_data)}")
print(f"✅ Commenti creati: {comments_count}")
print(f"✅ Download totali registrati: {db.torrents.aggregate([{'$group': {'_id': None, 'total': {'$sum': '$downloadCount'}}}])}")
print("\n🎉 Database popolato con successo!")
print("\nDati di accesso per il test:")
print("  Admin: admin@torrent.com / Admin123456")
print("  Moderator: moderator@torrent.com / Moderator123456")
print("  Utente: alice@torrent.com / Alice123456")
