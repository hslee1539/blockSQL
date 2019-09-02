import hashlib
import blockSQL

def createHash(iterable = (), hashFunc = hashlib.sha256) -> str:
    text = ""
    for item in iterable:
        text += str(item)
    return hashFunc(text.encode()).hexdigest()

def createData(key : str, iterable : tuple) -> str:
    text = ""
    for item in iterable:
        text += str(item) + " "
    return blockSQL.crypto.rc4_module.rc4_encrypt(key, text)

def decryptData(key : str, data : str) -> str:
    return blockSQL.crypto.rc4_module.rc4_encrypt(key, data)