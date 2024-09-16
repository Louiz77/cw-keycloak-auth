import secrets

def generate_token():
    return secrets.randbits(20)
