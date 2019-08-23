import hashlib
import sqlite3
import time
from Crypto.Cipher import ARC4

import blockSQL

def create(connection : sqlite3.Connection, hashFunc = hashlib.sha256, arc4 = ARC4.new):
    retval = connection.execute("SELECT name FROM sqlite_master WHERE type='table' and name='block';").fetchone()
    if (retval == None):
        connection.execute("""
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
        connection.execute("""
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

def insert(connection : sqlite3.Connection, tableName : str, hashFunc = hashlib.sha256, arc4 = ARC4.new, timeFunc = time.time) -> None:
    retval = connection.execute("""
    SELECT *
    FROM {0}_history
    WHERE history_isComplete IS NULL
    """.format(tableName)).fetchall()
    historyList = []
    for row in retval:
        row = list(row)
        row[2] = 1
        historyList.append(row)


    lastPreviousBlock = connection.execute("""
    SELECT history_id, tableName, data, hash, completeTime
    FROM block
    ORDER BY id DESC
    LIMIT 1
    """).fetchone()
    
    
    for row in historyList:
        previousHash = blockSQL.sql.tool.block_module.createHash(lastPreviousBlock, hashFunc)
        data = blockSQL.sql.tool.block_module.createData(previousHash, row, arc4)
        currentBlock = (row[0], tableName, data, previousHash, timeFunc())
        connection.execute("""
        INSERT INTO block (history_id, tableName, data, hash, completeTime)
        VALUES({0}, "{1}", "{2}", "{3}", {4})
        """.format(*currentBlock))
        lastPreviousBlock = currentBlock

    connection.execute("""
    UPDATE {0}_history
    SET history_isComplete = 1
    WHERE history_isComplete IS NULL
    """.format(tableName))

def check(connection : sqlite3.Connection, startID : int, endID : int, hashFunc = hashlib.sha256, arc4 = ARC4.new):
    """"""
    blockCursor = connection.execute("""
    SELECT history_id, tableName, data, hash, completeTime
    FROM block
    WHERE {0} <= id AND id < {1}
    """)

    previousHash

