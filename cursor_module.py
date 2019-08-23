import sqlite3
import time
import hashlib

DEBUG = False
Any = "any"
class Cursor:
    """sqlite3.Cursor에 대응되는 클래스입니다."""
    #fields
    _cursor_ : sqlite3.Cursor

    def __init__(self, cursor : sqlite3.Cursor):
        self._cursor_ = cursor

    def fetchone(self) -> Any:
        """None, 값, tuble 중 하나가 반환됩니다."""
        return self._cursor_.fetchone()
    
    def fetchall(self) -> list:
        """리스트를 반환합니다."""
        return self._cursor_.fetchall()
        
