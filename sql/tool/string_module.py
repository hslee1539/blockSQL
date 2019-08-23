

def removeHeadNoise(text : str, s = " ") -> str:
    count = 0
    l = len(s)
    for i in range(0, len(text), l):
        if(text[i:i + l] != s):
            break
        count += l
    return text[count:]

def removeEndNoise(text : str, s = " ") -> str:
    count = len(text)
    l = len(s)
    for i in range(count - l, -1, -l):
        if(s != text[i:i + l]):
            break
        count -= l
    return text[:count]

def getParenthesesContext(text : str, frontC = "(", endC = ")") -> str:
    """소괄호 내용을 찾습니다. 없으면 빈 str를 반환합니다."""
    start = text.find(frontC)
    end = -1
    if(start > -1):
        start += len(frontC)
        tmpEnd = text.find(endC, start)
        while(tmpEnd > -1):
            end = tmpEnd
            tmpEnd = text.find(endC, tmpEnd + len(endC))
        if(end == -1):
            start = -1
    return text[start : end]

def getParenthesesContext2(text : str, frontC = "(", endC = ")") -> str:
    """소괄호 내용을 찾습니다. 가장 먼저 발견된 endC까지를 반환합니다."""
    start = text.find(frontC)
    end = -1
    if(start > -1):
        start += len(frontC)
        end = text.find(endC, start)
        if(end == -1):
            start = -1
    return text[start : end]

def removeNoise(text : str) -> str:
    """탭과 줄바꿈 문자를 띄어 쓰기로 바꾸고 중첩 띄어 쓰기를 한번만 띄어지게 만듭니다."""
    text = text.replace("\n", " ").replace("\t", " ")

    tmp = text.replace("  ", " ")
    while(len(tmp) != len(text)):
        text = tmp
        tmp = tmp.replace("  ", " ")
    
    return text

def removeCommaNoise(text : str) -> str:
    tmp = text.replace(", ,", ",").replace(" , ", ",")
    while(len(tmp) != len(text)):
        text = tmp
        tmp = text.replace(", ,", ",").replace(" , ", ",")
    if(text[-1] == ","):
        text = text[:-1]
    if(text[-2:] == ", "):
        text = text[:-2]
    return text