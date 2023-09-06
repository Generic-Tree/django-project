def safe(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs) or None
        except:
            return None
    return wrapper
