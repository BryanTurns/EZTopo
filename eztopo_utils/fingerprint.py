import hashlib
# Generated from chatgpt
# Generates hash based on first n chunks. If n < 0 then do the whole file
def generateFingerprintFromFile(file_path, n):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        if n > 0:
            for i in range(n):
                chunk = file.read(4096)  # Read file in chunks
                if not chunk:
                    break
                hasher.update(chunk)
        else:
            while True:
                chunk = file.read(4096)  # Read file in chunks
                if not chunk:
                    break
                hasher.update(chunk)
    return hasher.hexdigest()

def generateFingerprintFromObject(obj):
    hasher = hashlib.sha256()
    while True:
        chunk = file.read(4096)  # Read file in chunks
        if not chunk:
            break
        hasher.update(chunk)