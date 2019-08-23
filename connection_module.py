import sqlite3
import time
import hashlib
from Crypto.Cipher import ARC4

import blockSQL


class Connection:
    """sqlite3.Connection에 대응되는 클래스입니다."""
    #fields
    _connection_ : sqlite3.Connection
    __cursor__ : blockSQL.cursor_module.Cursor
    _arc4 : ARC4.new
    _hashFunc : hashlib.sha256
    _tableInfo : blockSQL.sql.tool.table_info_module.TableInfo
    _timeFunc : time.time

    def __init__(self, database : str, arc4 = ARC4.new, hashFunc = hashlib.sha256, timeFunc = time.time):
        self._connection_ = sqlite3.connect(database)
        self.__cursor__ = blockSQL.Cursor(self._connection_.cursor())
        self._tableInfo = blockSQL.sql.tool.table_info_module.TableInfo(self._connection_.cursor())
        self._arc4 = arc4
        self._hashFunc = hashFunc
        self._timeFunc = timeFunc
        blockSQL.sql.block_module.create(self._connection_, hashFunc, arc4)
        
    def execute(self, sql : str) -> blockSQL.cursor_module.Cursor:
        sql = blockSQL.sql.sql_module.string_module.removeHeadNoise(sql)
        sql = blockSQL.sql.sql_module.string_module.removeHeadNoise(sql, '\n')
        funcName = blockSQL.sql.sql_module.findFunc(sql)
        if(funcName == "CREATE TABLE"):
            tableName = blockSQL.sql.sql_module.getInfo_create(sql)
            blockSQL.sql.currentTable_module.create(self._connection_, sql, tableName)
            blockSQL.sql.historyTable_module.create(self._connection_, tableName)
        elif(funcName == "INSERT INTO"):
            tableName, columns = blockSQL.sql.sql_module.getInfo_insert(sql, self._tableInfo)
            blockSQL.sql.currentTable_module.insert(self._connection_, sql, tableName)
            blockSQL.sql.historyTable_module.insert(self._connection_, tableName, columns, self._timeFunc)
            blockSQL.sql.block_module.insert(self._connection_, tableName, self._hashFunc, self._arc4, self._timeFunc)
            blockSQL.sql.currentTable_module.done(self._connection_, tableName)
        elif(funcName == "UPDATE"):
            tableName, columns, where = blockSQL.sql.sql_module.getInfo_update(sql, self._tableInfo)
            blockSQL.sql.currentTable_module.update(self._connection_, tableName, where, sql)
            blockSQL.sql.historyTable_module.insert(self._connection_, tableName, columns, self._timeFunc)
            blockSQL.sql.block_module.insert(self._connection_, tableName, self._hashFunc, self._arc4, self._timeFunc)
            blockSQL.sql.currentTable_module.done(self._connection_, tableName)
        else:
            self.cursor._cursor_ = self._connection_.execute(sql)
        return self.__cursor__


    @property
    def cursor(self):
        return self.__cursor__
        
    def commit(self):
        self._connection_.commit()
        return self

    def quickCheck(self, startID : int, endID):
        """변조를 빠르게 체크합니다"""
        
    def close(self):
        self._connection_.close()
