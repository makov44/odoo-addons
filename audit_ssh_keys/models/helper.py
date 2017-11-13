import hashlib


def generate_id(uri):
    hc = hashlib.sha256(str(uri).encode('utf-8'))
    return int(hc.hexdigest(), 16) % 10**15
