import hashlib
import sqlite3
import time
from Crypto.Cipher import ARC4

import blockSQL

def create(cursor : sqlite3.Cursor, hashFunc = hashlib.sha256, arc4 = ARC4.new):
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
        tmpData = blockSQL.sql.tool.block_module.createData(tmpHash, ["NoData"], arc4)
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

def insert(cursor : sqlite3.Cursor, tableName : str, hashFunc = hashlib.sha256, arc4 = ARC4.new, timeFunc = time.time) -> None:
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
    SELECT history_id, tableName, data, hash, completeTime
    FROM block
    ORDER BY id DESC
    LIMIT 1
    """).fetchone()
    
    
    for row in historyList:
        previousHash = blockSQL.sql.tool.block_module.createHash(lastPreviousBlock, hashFunc)
        data = blockSQL.sql.tool.block_module.createData(previousHash, row, arc4)
        currentBlock = (row[0], tableName, data, previousHash, timeFunc())
        cursor.execute("""
        INSERT INTO block (history_id, tableName, data, hash, completeTime)
        VALUES({0}, "{1}", "{2}", "{3}", {4})
        """.format(*currentBlock))
        lastPreviousBlock = currentBlock

    cursor.execute("""
    UPDATE {0}_history
    SET history_isComplete = 1
    WHERE history_isComplete IS NULL
    """.format(tableName))

def check(cursor : sqlite3.Cursor, startID : int, endID : int, hashFunc = hashlib.sha256, arc4 = ARC4.new):
    """"""
    blockCursor = cursor.execute("""
    SELECT history_id, tableName, data, hash, completeTime
    FROM block
    WHERE {0} <= id AND id < {1}
    """)

    previousHash

