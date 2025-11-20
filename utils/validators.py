import re

def validate_email(email):
    """Valida l'indirizzo email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Valida l'username"""
    if len(username) < 3 or len(username) > 50:
        return False
    pattern = r'^[a-zA-Z0-9_-]+$'
    return re.match(pattern, username) is not None

def validate_password(password):
    """Valida la password"""
    if len(password) < 8:
        return False
    # Password deve contenere almeno una lettera maiuscola, una minuscola e un numero
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit

def validate_torrent_title(title):
    """Valida il titolo del torrent"""
    return 3 <= len(title) <= 200

def validate_torrent_description(description):
    """Valida la descrizione del torrent"""
    return 10 <= len(description) <= 10000
