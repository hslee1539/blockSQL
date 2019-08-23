import time

def create():
    return "\
DECLARE @loginTime REAL; \
DECLARE @sqlTime REAL;"

def updateLoginTime(loginTime = time.time()) -> str:
    return "SET @loginTime = " + str(loginTime) + ";"

def updateSQLTime(sqlTime = time.time()) -> str:
    return "SET @sqlTime = " + str(sqlTime) + ";"