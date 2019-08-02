import sqlite3
import time
import hashlib

class Cursor:
    #fields
    _cursor_ : sqlite3.Cursor

    def __init__(self, cursor : sqlite3.Cursor):
        self._cursor_ = cursor
    
    def _addNewBlock_(self, sql : str):
        self._cursor_.execute("SELECT * FROM block order by id desc")
        fetch = self._cursor_.fetchone()
        print(fetch)
        newBlock_id = str(fetch[0] + 1)
        newBlock_sql = "'" + sql.replace("'", '"') + "'"
        newBlock_json = "''"
        newBlock_date = str(time.time())
        
        tmp = "blockSQL"
        for item in fetch:
            tmp += str(item)

        newBlock_hash = "'" + hashlib.sha256(tmp.encode()).digest().hex() + "'"

        print("insert into block values(" + newBlock_id + ', ' + newBlock_sql + ', ' + newBlock_json + ", " + newBlock_date + ", " + newBlock_hash +")")

        self._cursor_.execute("insert into block values(" + newBlock_id + ', ' + newBlock_sql + ', ' + newBlock_json + ", " + newBlock_date + ", " + newBlock_hash +")")

    def execute(self, sql : str):
        #sqls = decode(sql)
        #for sql in sqls:
        #    self._cursor_.execute(sql)
        self._addNewBlock_(sql)
        self._cursor_.execute(sql)
        return self
    
    def fetchone(self):
        return self._cursor_.fetchone()
    
    def fetchall(self):
        return self._cursor_.fetchall()
        
