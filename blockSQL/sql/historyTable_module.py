import sqlite3
import time

def create(connection : sqlite3.Connection, tableName : str)->None:
    """insert만 수행하는 히스토리 테이블을 만듭니다."""
    tmp = connection.execute("""
    PRAGMA table_info({0})""".format(tableName)).fetchall()

    columns = "{0} {1}".format(tmp[0][1] ,tmp[0][2])
    for i in range(1,len(tmp)):
        columns += ",{0} {1}".format(tmp[i][1] ,tmp[i][2])
    
    connection.execute("""
    CREATE TABLE {0}_history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        history_sqlTime REAL,
        history_isComplete INTEGER,
        {1}
    )""".format(tableName, columns))
    
def insert(connection : sqlite3.Connection, tableName : str, columns : str, timeFunc = time.time)->None:
    """해당 테이블의 current 테이블 내용을 추가합니다."""
    connection.execute("""
    INSERT INTO {0}_history (history_sqlTime, {1})
    SELECT {2}, *
    FROM {0}_current
    """.format(tableName, columns, timeFunc() ))
