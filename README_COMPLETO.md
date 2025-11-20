# 🌍 Piattaforma di Condivisione Torrent

Una piattaforma web completa per la condivisione e gestione di file torrent, sviluppata con Python Flask, MongoDB e JavaScript moderno.

## 📋 Caratteristiche Principali

### 👥 Gestione Utenti
- ✅ Registrazione e login con autenticazione JWT
- ✅ Ruoli differenziati: Guest, User, Moderator, Admin
- ✅ Profilo utente con storico torrent caricati
- ✅ Gestione della sicurezza con bcrypt

### 🎬 Gestione Torrent
- ✅ Caricamento di torrent con metadati completi
- ✅ Ricerca avanzata per titolo e descrizione
- ✅ Filtraggio per categoria
- ✅ Ordinamento per data, download count o dimensione
- ✅ Paginazione efficiente
- ✅ Tracciamento download
- ✅ Visualizzazione dettagliata con commenti

### 💬 Sistema di Commenti
- ✅ Aggiunta di commenti con valutazione (1-5 stelle)
- ✅ Modifica e eliminazione dei propri commenti
- ✅ Moderazione admin dei commenti

### 📊 Pannello Amministrativo
- ✅ Dashboard con statistiche globali
- ✅ Gestione utenti (cambio ruolo, ban)
- ✅ Analisi torrent più popolari
- ✅ Statistiche per categoria
- ✅ Monitoraggio attività settimanale

### 🎨 Interfaccia Utente
- ✅ Design moderno e responsivo
- ✅ Tema chiaro e intuitivo
- ✅ Notifiche in tempo reale
- ✅ Grid layout per torrent
- ✅ Navigazione fluida

## 🚀 Installazione

### Prerequisiti
- Python 3.7+
- MongoDB Atlas (o MongoDB locale)
- pip

### Passi di Installazione

1. **Clona il repository**
```bash
git clone <repository-url>
cd torrent-platform1
```

2. **Crea un ambiente virtuale**
```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

3. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```

4. **Configura le variabili d'ambiente**
```bash
cp .env.example .env
```

Edita il file `.env` con le tue credenziali MongoDB:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=app
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. **Popola il database con dati di test (opzionale)**
```bash
python seed_db.py
```

6. **Avvia il server**
```bash
python app.py
```

L'applicazione sarà disponibile su `http://localhost:5000`

## 📁 Struttura del Progetto

```
torrent-platform/
├── app.py                          # Entry point Flask
├── config.py                       # Configurazione
├── requirements.txt                # Dipendenze
├── seed_db.py                      # Script per popolare il database
├── .env.example                    # Template variabili d'ambiente
├── .gitignore                      # File da escludere da Git
│
├── models/                         # Modelli dati
│   ├── user.py                    # Model User
│   ├── torrent.py                 # Model Torrent
│   ├── comment.py                 # Model Comment
│   └── category.py                # Model Category
│
├── routes/                         # API Routes
│   ├── auth.py                    # Auth routes (login, register)
│   ├── torrents.py                # Torrent CRUD
│   ├── comments.py                # Comment CRUD
│   └── admin.py                   # Admin dashboard
│
├── utils/                          # Utility functions
│   ├── auth.py                    # JWT e decorators
│   ├── validators.py              # Validazioni input
│   └── helpers.py                 # Helper functions
│
├── templates/                      # HTML templates
│   ├── base.html                  # Template base
│   ├── index.html                 # Homepage
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── torrent_detail.html        # Dettagli torrent
│   ├── upload.html                # Upload form
│   ├── profile.html               # User profile
│   └── admin.html                 # Admin dashboard
│
└── static/                         # File statici
    ├── css/
    │   └── style.css              # Stili globali
    └── js/
        └── app.js                 # Logica client
```

## 🔐 Credenziali di Test

Se hai eseguito `python seed_db.py`, puoi usare questi account:

### Admin
- **Email:** admin@torrent.com
- **Password:** Admin123456

### Moderator
- **Email:** moderator@torrent.com
- **Password:** Moderator123456

### Utente Standard
- **Email:** alice@torrent.com
- **Password:** Alice123456

## 📚 API Endpoints

### Autenticazione
- `POST /api/register` - Registrazione nuovo utente
- `POST /api/login` - Login utente
- `GET /api/profile` - Profilo utente (richiede auth)

### Torrent
- `GET /api/torrents` - Lista torrent con filtri e paginazione
- `GET /api/torrents/<id>` - Dettagli torrent
- `POST /api/torrents` - Carica nuovo torrent (richiede auth)
- `POST /api/torrents/<id>/download` - Registra download (richiede auth)

### Commenti
- `POST /api/torrents/<id>/comments` - Aggiungi commento (richiede auth)
- `PUT /api/comments/<id>` - Modifica commento (richiede auth)
- `DELETE /api/comments/<id>` - Elimina commento (richiede auth)

### Admin
- `GET /api/admin/stats` - Statistiche (richiede admin)
- `GET /api/admin/users` - Lista utenti (richiede admin)
- `PUT /api/admin/users/<id>/role` - Cambio ruolo (richiede admin)
- `PUT /api/admin/users/<id>/ban` - Ban/unban utente (richiede admin)

## 🔒 Sistema di Ruoli

| Ruolo | Privilegi |
|-------|-----------|
| **Guest** | Visualizzare torrent, registrarsi/login |
| **User** | Guest + Caricare torrent, commentare, scaricare |
| **Moderator** | User + Moderare commenti |
| **Admin** | Moderator + Gestire utenti, statistiche, ban |

## 🛠️ Tecnologie Utilizzate

### Backend
- **Flask 2.3.3** - Framework web Python
- **PyMongo 4.5.0** - Driver MongoDB
- **bcrypt 4.0.1** - Hashing password
- **PyJWT 2.8.0** - Token JWT
- **python-dotenv** - Gestione variabili d'ambiente

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling responsive
- **JavaScript ES6+** - Logica client
- **Fetch API** - Comunicazione API

### Database
- **MongoDB Atlas** - Database cloud
- **Indici** per performance

## 📖 Guida all'Uso

### Per gli Utenti
1. Registrati con email e password valida
2. Accedi alla piattaforma
3. Visualizza i torrent disponibili
4. Cerca per titolo, categoria o ordinamento
5. Scarica i torrent preferiti
6. Commenta e valuta i torrent
7. Visualizza il tuo profilo e i tuoi upload

### Per gli Admin
1. Accedi come admin
2. Vai nel pannello di amministrazione
3. Visualizza statistiche globali
4. Gestisci utenti (cambio ruolo, ban)
5. Monitora l'attività della piattaforma

## 🐛 Troubleshooting

### Errore di connessione MongoDB
- Verifica che il `MONGO_URI` nel `.env` sia corretto
- Controlla che MongoDB Atlas sia accessibile
- Assicurati che l'IP della tua macchina sia whitelist in MongoDB Atlas

### Errore di autorizzazione
- Verifica che il token JWT sia valido
- Controlla che l'header Authorization sia correttamente formattato
- Accertati di avere i permessi necessari per l'azione

### API restituisce 500
- Controlla i log della console Flask
- Verifica che i dati inviati siano nel formato corretto
- Assicurati che le collezioni MongoDB esistano

## 🔄 Prossimi Miglioramenti

- [ ] Upload file torrent effettivo
- [ ] Torrent streaming
- [ ] Sistema di rating più avanzato
- [ ] Notifiche email
- [ ] Backup automatico
- [ ] API cache
- [ ] Progressive Web App

## 📝 Licenza

Questo progetto è disponibile sotto licenza MIT.

## 👨‍💻 Autore

Sviluppato come piattaforma di condivisione file torrent completa.

## 📧 Contatti e Supporto

Per supporto, contatta l'amministratore della piattaforma.

**lo schema JSON delle collezioni**
---

## **1️⃣ Collection: users**

Ogni utente ha:

* `username` unico
* `email` unico
* `passwordHash` (lo script usa la funzione `User.create_user`)
* `role` (admin, moderator, user)
* `banned` (opzionale, default `False`)
* `createdAt` (data creazione)

```json
{
  "bsonType": "object",
  "required": ["username", "email", "passwordHash", "role", "createdAt", "banned"],
  "properties": {
    "username": {
      "bsonType": "string",
      "description": "Nome univoco dell'utente"
    },
    "email": {
      "bsonType": "string",
      "pattern": "^.+@.+\\..+$",
      "description": "Email dell'utente"
    },
    "passwordHash": {
      "bsonType": "string",
      "description": "Hash della password"
    },
    "role": {
      "bsonType": "string",
      "enum": ["guest", "user", "moderator", "admin"],
      "description": "Ruolo dell'utente"
    },
    "banned": {
      "bsonType": "bool",
      "description": "Indica se l'utente è stato bannato"
    },
    "createdAt": {
      "bsonType": "date",
      "description": "Data registrazione"
    }
  }
}
```

---

## **2️⃣ Collection: torrents**

Ogni torrent ha:

* `title`
* `description` max 160 caratteri
* `size` in MB/GB
* `categories` array
* `images` array
* `uploaderId` riferimento a `users._id`
* `torrentFilePath`
* `downloadCount` intero
* `createdAt` data creazione

```json
{
  "bsonType": "object",
  "required": ["title", "description", "size", "categories", "uploaderId", "torrentFilePath", "downloadCount", "createdAt"],
  "properties": {
    "title": { "bsonType": "string" },
    "description": { "bsonType": "string", "maxLength": 160 },
    "size": { "bsonType": "int", "minimum": 0 },
    "categories": { "bsonType": "array", "items": { "bsonType": "string" } },
    "images": { "bsonType": "array", "items": { "bsonType": "string" } },
    "uploaderId": { "bsonType": "objectId" },
    "torrentFilePath": { "bsonType": "string" },
    "downloadCount": { "bsonType": "int", "minimum": 0 },
    "createdAt": { "bsonType": "date" }
  }
}
```

---

## **3️⃣ Collection: comments**

Ogni commento ha:

* `torrentId` riferimento a `torrents._id`
* `userId` riferimento a `users._id`
* `text` max 160 caratteri
* `rating` da 1 a 5
* `createdAt` data creazione
* `updatedAt` data ultima modifica

```json
{
  "bsonType": "object",
  "required": ["torrentId", "userId", "text", "rating", "createdAt"],
  "properties": {
    "torrentId": { "bsonType": "objectId" },
    "userId": { "bsonType": "objectId" },
    "text": { "bsonType": "string", "maxLength": 160 },
    "rating": { "bsonType": "int", "minimum": 1, "maximum": 5 },
    "createdAt": { "bsonType": "date" },
    "updatedAt": { "bsonType": "date" }
  }
}
```

---

## **Nota**

* Lo script aggiunge anche un campo `downloadCount` per i torrent.
* I campi `images` e `categories` sono array di stringhe.
* L’ID dell’utente e del torrent sono **ObjectId di MongoDB**, quindi bisogna usare `.toString()` lato frontend per confronti.

---

Se vuoi, posso creare **uno schema JSON completo pronto da importare in MongoDB Atlas** tramite la funzione di validazione JSON Schema per tutte e tre le collezioni, così il tuo database sarà completamente strutturato e protetto.

Vuoi che faccia anche questo?
