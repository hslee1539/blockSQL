import sqlite3
import time
import hashlib

import blockSQL

Any = "any"
class Cursor:
    """sqlite3.Cursor에 대응되는 클래스입니다."""
    #fields
    _cursor_ : sqlite3.Cursor

    def __init__(self, cursor : sqlite3.Cursor, tableInfo : blockSQL.sql.tool.table_info_module, hashFunc = hashlib.sha256, timeFunc = time.time):
        self._cursor_ = cursor
        self._tableInfo = tableInfo
        self._hashFunc = hashFunc
        self._timeFunc = timeFunc
        self.description = cursor.description
    
    def execute(self, sql : str) :
        blockSQL.execution_module.execute(self._cursor_, sql, self._tableInfo, self._hashFunc, self._timeFunc)
        self.description = self._cursor_.description
        return self

    def fetchone(self) -> Any:
        """None, 값, tuble 중 하나가 반환됩니다."""
        return self._cursor_.fetchone()
    
    def fetchall(self) -> list:
        """리스트를 반환합니다."""
        return self._cursor_.fetchall()

    def fetch_tkinter(self, titleName = "blockSQL table viewer") -> blockSQL.graphic.window_module.TableWindow:
        retval = self._cursor_.fetchall()
        if(len(retval) == 0):
            retval = [["None"]]
        return blockSQL.graphic.window_module.TableWindow(self.description, retval, titleName)
    
    def close(self) -> None:
        self._cursor_.close()
        
