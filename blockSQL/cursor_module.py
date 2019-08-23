import sqlite3
import time
import hashlib

from blockSQL import BlockSQL
DEBUG = False
Any = "any"
class Cursor:
    """sqlite3.Cursor에 대응되는 클래스입니다."""
    #fields
    _cursor_ : sqlite3.Cursor
    blockSQL = BlockSQL()

    def __init__(self, cursor : sqlite3.Cursor):
        self._cursor_ = cursor
        self.blockSQL.login()

    def execute(self, sql : str):
        """쿼리를 실행하고 블록에 기록합니다."""
        tmpStr = self.blockSQL.insert(sql.replace("'", '"'), "None", time.time())
        if DEBUG:
            print(tmpStr)
        self._cursor_.execute(tmpStr)
        # 나중에 connection을 분리하자!
        self._cursor_.execute(sql)
        return self

    def fetchone(self) -> Any:
        """None, 값, tuble 중 하나가 반환됩니다."""
        return self._cursor_.fetchone()
    
    def fetchall(self) -> list:
        """리스트를 반환합니다."""
        return self._cursor_.fetchall()
        
