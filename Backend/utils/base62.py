import string

BASE62 = string.ascii_letters + string.digits

def encode_base62(number):
    if number == 0:
        return "0"

    result = ""

    while number > 0:
        index = number % 62
        result = BASE62[index] + result
        number //= 62

    return result

def decode_base62(code):
    number = 0

    for char in code:
        val = BASE62.index(char)
        number = number * 62 + val

    return number
