import hashlib
import Crypto.Cipher.ARC4

def createHash(iterable = (), hashFunc = hashlib.sha256) -> str:
    text = ""
    for item in iterable:
        text += str(item)
    return hashFunc(text.encode()).hexdigest()

def createData(key : str, iterable : tuple, arc4 = Crypto.Cipher.ARC4.new) -> str:
    text = ""
    for item in iterable:
        text += str(item) + " "
    return arc4(key.encode()).encrypt(text.encode()).hex()

def decryptData(key : str, data : str, arc4 = Crypto.Cipher.ARC4.new) -> str:
    return arc4(key.encode()).decrypt(bytes.fromhex(data)).decode()