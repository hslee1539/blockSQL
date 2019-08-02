from blockSQL import Cursor

import sqlite3


class Connection:
    #fields
    _connection_ : sqlite3.Connection
    __cursor__ : Cursor

    def __init__(self, database : str):
        self._connection_ = sqlite3.connect(database)
        tmpCursor = self._connection_.cursor()
        self.__cursor__ = Cursor(tmpCursor)


        tmpCursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='block'")
        tmp = tmpCursor.fetchone()
        print(tmp)
        if(tmp == None):
            print("ok")
            tmpCursor.execute("create table block(id int, sql text, json text, date real, hash text)")
            self._connection_.commit()
            tmpCursor.execute("insert into block values(0, ' ', ' ', 1564587533.5644205, ' ');")
            self._connection_.commit()
        


    @property
    def cursor(self):
        return self.__cursor__
        
    def commit(self):
        self._connection_.commit()
    
    def close(self):
        self._connection_.close()
