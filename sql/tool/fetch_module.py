import sqlite3

NoneOrTuple = ""

def fetchoneGenerator(cursor : sqlite3.Cursor) -> NoneOrTuple:
    """fetchone을 수행하는 제너레이터입니다."""
    retval = cursor.fetchone()
    while(retval != None):
        yield retval
        retval = cursor.fetchone()