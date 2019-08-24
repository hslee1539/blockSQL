import sqlite3
import time
import hashlib
from Crypto.Cipher import ARC4

import blockSQL


class Connection:
    """sqlite3.Connection에 대응되는 클래스입니다."""
    #fields
    _connection_ : sqlite3.Connection
    _arc4 : ARC4.new
    _hashFunc : hashlib.sha256
    _tableInfo : blockSQL.sql.tool.table_info_module.TableInfo
    _timeFunc : time.time

    def __init__(self, database : str, arc4 = ARC4.new, hashFunc = hashlib.sha256, timeFunc = time.time):
        self._connection_ = sqlite3.connect(database)
        tmpCursor = self._connection_.cursor()
        self._tableInfo = blockSQL.sql.tool.table_info_module.TableInfo(tmpCursor)
        self._arc4 = arc4
        self._hashFunc = hashFunc
        self._timeFunc = timeFunc
        blockSQL.sql.block_module.create(tmpCursor, hashFunc, arc4)

    def cursor(self):
        return blockSQL.Cursor(self._connection_.cursor(), self._tableInfo, self._arc4, self._hashFunc, self._timeFunc)
        
    def execute(self, sql : str) -> blockSQL.cursor_module.Cursor:
        return blockSQL.Cursor(blockSQL.execution_module.execute(self._connection_.cursor(), sql, self._tableInfo, self._arc4, self._hashFunc,self._timeFunc), self._tableInfo, self._arc4, self._hashFunc, self._timeFunc)
        
    def commit(self):
        self._connection_.commit()
        return self

    def quickCheck(self, startID : int, endID):
        """변조를 빠르게 체크합니다"""
        
    def close(self):
        self._connection_.close()
