import hashlib
import sqlite3
import time

import blockSQL

def create(cursor : sqlite3.Cursor, hashFunc = hashlib.sha256):
    retval = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='block';").fetchone()
    if (retval == None):
        cursor.execute("""
        CREATE TABLE block(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            history_id INTEGER,
            tableName TEXT,
            data TEXT,
            hash TEXT,
            completeTime REAL
        );
        """)
        tmpHash = blockSQL.sql.tool.block_module.createHash(["NoData"], hashFunc)
        tmpData = blockSQL.sql.tool.block_module.createData(tmpHash, ["NoData"])
        cursor.execute("""
        INSERT INTO block
        VALUES(
            0,
            0,
            "noTable",
            "{0}",
            "{1}",
            0.0
        );
        """.format(tmpData, tmpHash))

def insert(cursor : sqlite3.Cursor, tableName : str, hashFunc = hashlib.sha256, timeFunc = time.time) -> None:
    retval = cursor.execute("""
    SELECT *
    FROM {0}_history
    WHERE history_isComplete IS NULL
    """.format(tableName)).fetchall()
    historyList = []
    for row in retval:
        row = list(row)
        row[2] = 1
        historyList.append(row)


    lastPreviousBlock = cursor.execute("""
    SELECT *
    FROM block
    ORDER BY id DESC
    LIMIT 1
    """).fetchone()
    
    
    for row in historyList:
        previousHash = blockSQL.sql.tool.block_module.createHash(lastPreviousBlock, hashFunc)
        data = blockSQL.sql.tool.block_module.createData(previousHash, row)
        currentBlock = (lastPreviousBlock[0] + 1, row[0], tableName, data, previousHash, timeFunc())
        cursor.execute("""
        INSERT INTO block
        VALUES({0}, {1}, "{2}", "{3}", "{4}", {5})
        """.format(*currentBlock))
        lastPreviousBlock = currentBlock

    cursor.execute("""
    UPDATE {0}_history
    SET history_isComplete = 1
    WHERE history_isComplete IS NULL
    """.format(tableName))

def checkFast(cursor : sqlite3.Cursor, startID : int, endID : int, hashFunc = hashlib.sha256, closeCursor = True) -> int:
    """블록들의 해시를 검사합니다. 오류가 없을 시, startID, 오류가 있을 시, 해당 id를 반환합니다."""
    cursor.execute("""
    SELECT *
    FROM block
    WHERE {0} <= id AND id < {1}
    """.format(startID, endID))
    retval = startID
    gen = blockSQL.sql.tool.fetch_module.fetchoneGenerator(cursor)

    previousHash = blockSQL.sql.tool.block_module.createHash(next(gen), hashFunc)
    for row in gen:
        if(row[4] != previousHash):
            retval = row[0]
            break
        previousHash = blockSQL.sql.tool.block_module.createHash(row, hashFunc)
    if(closeCursor):
        cursor.close()
    return retval
    

