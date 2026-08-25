from database import get_connection
from utils.base62 import encode_base62, decode_base62
import redis 

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

def shorten_url(original_url):
    conn = get_connection()

    id = conn.execute(
        "SELECT id FROM urls WHERE original_url = (?)",
        (original_url,)
    ).fetchone()

    if id is None:
        cursor = conn.execute(
            "INSERT INTO urls (original_url) VALUES (?)", 
            (original_url,)
        )
        conn.commit()

        url_id = cursor.lastrowid
    else:
        url_id = id[0]
    conn.close()

    code = encode_base62(url_id)
    r.set(f"url:{code}", original_url, ex=60)

    return code


def get_original_url(code):
    cached_url = r.get(f"url:{code}")
    if cached_url is not None:
        print(f"Cache hit for code: {code}")
        return cached_url
    
    url_id = decode_base62(code)

    conn = get_connection()

    original_url = conn.execute(
        "SELECT original_url FROM urls WHERE id = (?)",
        (url_id,)
    ).fetchone()

    conn.close
    if original_url is None:
        print(f"Cache miss for code: {code}. URL not found in database.")
        return None

    r.set(f"url:{code}", original_url[0], ex=60)
    print("Cache miss for code: {code}. Fetched from database and cached.")
    return original_url[0]


