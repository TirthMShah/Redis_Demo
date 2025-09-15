import hashlib
from django.utils.encoding import force_bytes



def generate_cache_key(prefix: str, user: str, query_string: str) -> str:
    """
    Generate a unique cache key using prefix, user, and query string.
    """
    key_base = f"{prefix}:{user}:{query_string}"
    cache_key = prefix + ':' + hashlib.md5(force_bytes(key_base)).hexdigest()
    return cache_key