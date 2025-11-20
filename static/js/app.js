class TorrentApp {
    constructor() {
        this.token = localStorage.getItem('token');
        this.currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateUI();
    }

    setupEventListeners() {
        // Navbar toggle
        const navToggle = document.getElementById('navToggle');
        const navLinks = document.getElementById('navLinks');
        if (navToggle && navLinks) {
            navToggle.addEventListener('click', (e) => {
                e.preventDefault();
                navLinks.classList.toggle('open');
                navToggle.classList.toggle('open');
            });
            // close menu on outside click
            document.addEventListener('click', (ev) => {
                if (!navLinks.contains(ev.target) && !navToggle.contains(ev.target)) {
                    navLinks.classList.remove('open');
                    navToggle.classList.remove('open');
                }
            });
        }

        // Logout
        const logoutBtn = document.getElementById('logout');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        }

        // Gestione form di login/registrazione
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');
        const uploadForm = document.getElementById('uploadForm');

        if (loginForm) loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        if (registerForm) registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        if (uploadForm) uploadForm.addEventListener('submit', (e) => this.handleUpload(e));
    }

    async apiCall(endpoint, options = {}) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options
        };

        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(endpoint, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Errore nella richiesta');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            this.showNotification(error.message, 'error');
            throw error;
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        try {
            const result = await this.apiCall('/api/login', {
                method: 'POST',
                body: JSON.stringify(data)
            });

            this.token = result.token;
            this.currentUser = result.user;

            localStorage.setItem('token', this.token);
            localStorage.setItem('currentUser', JSON.stringify(this.currentUser));

            this.showNotification('Login effettuato con successo!', 'success');
            setTimeout(() => window.location.href = '/', 1000);
        } catch (error) {
            // Gestione errore già gestita in apiCall
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        try {
            await this.apiCall('/api/register', {
                method: 'POST',
                body: JSON.stringify(data)
            });

            this.showNotification('Registrazione completata! Ora puoi effettuare il login.', 'success');
            setTimeout(() => window.location.href = '/login', 2000);
        } catch (error) {
            // Gestione errore già gestita in apiCall
        }
    }

    async handleUpload(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        // Converti le categorie da stringa a array
        if (data.categories) {
            data.categories = data.categories.split(',').map(cat => cat.trim());
        }

        try {
            await this.apiCall('/api/torrents', {
                method: 'POST',
                body: JSON.stringify(data)
            });

            this.showNotification('Torrent caricato con successo!', 'success');
            e.target.reset();
            setTimeout(() => window.location.href = '/', 2000);
        } catch (error) {
            // Gestione errore già gestita in apiCall
        }
    }

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('currentUser');
        this.token = null;
        this.currentUser = null;
        this.showNotification('Logout effettuato con successo!', 'success');
        setTimeout(() => window.location.href = '/', 1000);
    }

    updateUI() {
        // Aggiorna l'interfaccia in base allo stato di autenticazione
        const authElements = document.querySelectorAll('.auth-only');
        const guestElements = document.querySelectorAll('.guest-only');

        if (this.currentUser) {
            authElements.forEach(el => el.style.display = 'block');
            guestElements.forEach(el => el.style.display = 'none');
            
            // Mostra il menu admin se l'utente è admin
            if (this.currentUser.role === 'admin' || this.currentUser.role === 'moderator') {
                const adminMenu = document.getElementById('admin-menu');
                if (adminMenu) {
                    adminMenu.style.display = 'flex';
                }
            }
        } else {
            authElements.forEach(el => el.style.display = 'none');
            guestElements.forEach(el => el.style.display = 'block');
        }

        // Update nav auth visibility (for base.html new structure)
        document.querySelectorAll('.auth-only').forEach(el => el.style.display = this.currentUser ? 'inline-flex' : 'none');
        document.querySelectorAll('.guest-only').forEach(el => el.style.display = this.currentUser ? 'none' : 'inline-flex');
    }

    showNotification(message, type = 'info') {
        // Implementazione base delle notifiche
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            z-index: 1000;
            font-weight: bold;
        `;

        if (type === 'success') notification.style.backgroundColor = '#4CAF50';
        else if (type === 'error') notification.style.backgroundColor = '#f44336';
        else notification.style.backgroundColor = '#2196F3';

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // Utility: reveal elements on scroll (simple)
    enableRevealOnScroll() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('reveal');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        document.querySelectorAll('.torrent-card, .profile-card').forEach(el => observer.observe(el));
    }
}

// Inizializza l'app quando il DOM è pronto
document.addEventListener('DOMContentLoaded', () => {
    window.torrentApp = new TorrentApp();
    // enable reveal animations
    setTimeout(() => { if (window.torrentApp) window.torrentApp.enableRevealOnScroll(); }, 300);
});
