def rc4(key : str, data : bytearray, encoding = "utf-8") -> bytearray:
    """rc4 대칭키 알고리즘을 수행합니다.
    암호화 할때 평문을 data에 넣고, 해독할때, 암호문을 data에 넣습니다.

    param key : str
    (키를 문자열로 받습니다. 문자열의 인덱스가 128 이상부터는 의미가 없어 집니다.)

    param data : bytearray
    (암호문 또는 평문을 바이트 배열로 받습니다.)

    param encoding : str
    (문자열 포멧을 문자열로 받습니다.)

    return -> bytearray
    (data를 반환합니다.)
    """
    
    # python2에서는 결과가 다름
    # python3 기준임
    keyMap = key.encode(encoding)
    swapIndex = 0
    ksaKey = list(range(256))
    for i in range(256):
        #스왑 규칙
        swapIndex = (swapIndex + ksaKey[i] + keyMap[i % len(keyMap)]) % 256
        #스왑
        ksaKey[i], ksaKey[swapIndex] = ksaKey[swapIndex], ksaKey[i]

    
    dataMap = data
    swapIndex = 0
    swapIndex2 = 0
    for i in range(len(dataMap)):
        #스왑 규칙2
        swapIndex = (swapIndex + 1) % 256
        swapIndex2 = (swapIndex2 + ksaKey[swapIndex]) % 256
        #스왑2
        ksaKey[swapIndex], ksaKey[swapIndex2] = ksaKey[swapIndex2], ksaKey[swapIndex]
        #데이터와 xor 연산으로 암호화 및 복호화
        dataMap[i] ^= ksaKey[(ksaKey[swapIndex] + ksaKey[swapIndex2])%256]
    
    return dataMap

def rc4_encrypt(key : str, data : str, encoding = "utf-8") -> str:
    """rc4 대칭키 알고리즘을 수행합니다."""
    return rc4(key, bytearray(data.encode(encoding)), encoding).hex()

def rc4_decrypt(key : str, data : str, encoding = "utf-8") -> str:
    return rc4(key, bytearray.fromhex(data), encoding).decode(encoding)
