from datetime import datetime

def format_file_size(bytes_size):
    """Converte i bytes in formato leggibile"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def format_datetime(dt):
    """Formatta la data e l'ora"""
    if isinstance(dt, datetime):
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    return str(dt)

def calculate_time_ago(dt):
    """Calcola il tempo trascorso da una data"""
    if not isinstance(dt, datetime):
        return "Data non valida"
    
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)} secondi fa"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minuti fa"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} ore fa"
    elif seconds < 604800:
        days = int(seconds // 86400)
        return f"{days} giorni fa"
    else:
        weeks = int(seconds // 604800)
        return f"{weeks} settimane fa"

def truncate_text(text, length=100):
    """Tronca il testo a una lunghezza specifica"""
    if len(text) <= length:
        return text
    return text[:length] + "..."
