import time

def loading() -> str:
    return "SELECT name FROM sqlite_master WHERE type='table' and name='block';\
DECLARE @loginTime REAL; \
DECLARE @sqlTime REAL; \
DECLARE @blockID INT;"

def updateLoginTime(loginTime = time.time()) -> str:
    return "SET @loginTime = " + str(loginTime) + ";"

def updateSQLTime(sqlTime = time.time()) -> str:
    return "SET @sqlTime = " + str(sqlTime) + ";"

def updateBlockID() -> str:
    return "SET @blockID = (SELECT MAX(blockID) FROM block);"

def nextBlockID() -> str:
    return "SET @blockID = @blockID + 1"

def login(loginTime = time.time()) -> str:
    return updateLoginTime(loginTime) + updateBlockID()

def create() -> str:
    return "\
CREATE TABLE block (\
    loginTime REAL NOT NULL, \
    sqlTime REAL NOT NULL, \
    blockID INT, \
    sql TEXT, \
    json TEXT, \
    branchHash TEXT, \
    mergeHash TEXT, \
    PRIMARY KEY(loginTime, sqlTime)\
);\
INSERT INTO block(\
    loginTime,\
    sqlTime,\
    blockID\
) VALUES(\
    0.0,\
    0.0\
    0\
)"

def insert(sql : str, json : str) -> str:
    return "\
INSERT INTO block(\
    loginTime,\
    sqlTime,\
    sql,\
    json,\
) VALUES (\
    @loginTime,\
    @sqlTime,"\
    + sql + ","\
    + json +\
");"

def selectBranch() -> str:
    return "\
SELECT loginTime, sqlTime, sql, json \
FROM block \
WHERE blockID = (\
        SELECT MAX(blockID) \
        FROM block \
    ) OR \
    blockID IS NULL \
    AND loginTime = @loginTime \
ORDER BY blockID nulls last, sqlTime;"

def selectMerge() -> str:
    return "\
SELECT loginTime, sqlTime, sql, json, branchHash\
FROM block \
WHERE @loginTime = (\
        SELECT MIN(loginTime) \
        FROM block\
        WHERE blockID IS NULL\
    ) AND \
    "