import string
import secrets


def get_hash():
    alphabet = string.ascii_uppercase + string.digits
    hash = ''.join(secrets.choice(alphabet) for i in range(6))
    return hash
