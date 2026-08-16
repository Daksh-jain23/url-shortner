from database import get_connection
from utils.base62 import encode_base62, decode_base62

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

    return encode_base62(url_id)


def get_original_url(code):
    url_id = decode_base62(code)

    conn = get_connection()

    original_url = conn.execute(
        "SELECT original_url FROM urls WHERE id = (?)",
        (url_id,)
    ).fetchone()

    conn.close
    if original_url is None:
        return None
    return original_url[0]


