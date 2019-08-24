import sqlite3

def create(cursor : sqlite3.Cursor, sql : str, tableName : str) -> None:
    """해당 테이블과 해당 테이블의 _current 테이블을 생성합니다."""
    cursor.execute(sql.replace(tableName, tableName + "_current", 1))
    cursor.execute(sql)
    
def insert(cursor : sqlite3.Cursor, sql : str, tableName : str) -> None:
    """해당 테이블과 해당 테이블의 _current 테이블에 insert 합니다.
    이 함수 전 또는 후에 done()을 해야 합니다."""
    cursor.execute(sql.replace(tableName, tableName + "_current", 1))
    cursor.execute(sql)

def update(cursor : sqlite3.Cursor, tableName : str, where : str, sql : str) -> None:
    """해당 테이블과 해당 테이블의 _current 테이블을 업데이트 합니다.
    update를 하기 위해, _current 테이블에 해당 where문에 해당되는 것을 추가하고 _cureent 테이블을 업데이트 합니다.
    이 함수 전 또는 후에 done()을 해야 합니다."""
    cursor.execute("""
    INSERT INTO {0}_current
    SELECT *
    FROM {0}
    WHERE {1}""".format(tableName, where))
    
    cursor.execute(sql.replace(tableName, tableName + "_current", 1))
    cursor.execute(sql)
    
def done(cursor : sqlite3.Cursor, tableName : str) -> None:
    """_current 테이블의 모든 row를 삭제합니다. 이 함수를 제외한 모든 _current 연산은 기본적으로 row가 없는 것을 전제하기 때문에,
    다른 모든 연산들은 전 또는 후에 done()를 해야 합니다."""
    cursor.execute("""
    DELETE FROM {0}_current""".format(tableName))

