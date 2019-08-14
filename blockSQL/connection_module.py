from blockSQL import BlockSQL
from blockSQL import Cursor

import sqlite3
import time


class Connection:
    """sqlite3.Connection에 대응되는 클래스입니다."""
    #fields
    _connection_ : sqlite3.Connection
    _system_ : sqlite3.Connection
    __cursor__ : Cursor
    __cur__ : sqlite3.Cursor

    def __init__(self, database : str):
        self._connection_ = sqlite3.connect(database)
        self._system_ = sqlite3.connect(database)
        tmpCursor = self._connection_.cursor()
        self.__cursor__ = Cursor(tmpCursor)
        self.__cur__ = tmpCursor


        tmpCursor.execute(self.__cursor__.blockSQL.isCreate())
        tmp = tmpCursor.fetchone()
        if(tmp == None):
            tmpStr = self.__cursor__.blockSQL.create(time.time())
            tmpCursor.execute(tmpStr[0])
            tmpCursor.execute(tmpStr[1])
            self._connection_.commit()


    @property
    def cursor(self):
        return self.__cursor__
        
    def commit(self):
        """커밋과 동시에 블록을 완성합니다."""
        self._connection_.commit()
        sysCursor = self._system_.execute(self.__cursor__.blockSQL.selectBranch())
        finishBranch = sysCursor.fetchone()
        result = sysCursor.fetchone()
        
        while(result != None):
            result = list(result)
            result[4] = BlockSQL.createBranchHash(result[0], result[1], result[2], result[3], finishBranch[4])
            self._connection_.execute(BlockSQL.updateBranch(result[0], result[1], result[4]))
            finishBranch = result
            result = sysCursor.fetchone()
        
        self._connection_.commit()

        sysCursor = self._system_.execute(self.__cursor__.blockSQL.selectMerge())
        finishMerge = sysCursor.fetchone()
        result = sysCursor.fetchone()
        if(result != None):
            self.__cursor__.blockSQL.login()
            print(finishBranch)
        while(result != None):
            result = list(result)
            result[2] = time.time()
            result[6] = BlockSQL.createMergeHash(result[0], result[1], result[2], result[3], result[4], result[5], finishMerge[6])
            self._connection_.execute(BlockSQL.updateMerge(result[0], result[1], result[2], result[6]))
            finishMerge = result
            result = sysCursor.fetchone()
        self._connection_.commit()
        return self

    
    def close(self):
        self._connection_.close()
