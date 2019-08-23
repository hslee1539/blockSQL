from blockSQL.sql.tool import string_module, table_info_module
#import blockSQL
#import blockSQL.sql
#import string_module
#import blockSQL.sql.tool.table_info_module

def findFunc(sql : str)->str:
    insert_into = sql.find("INSERT INTO")
    if(sql.find("INSERT INTO") == 0):
        return "INSERT INTO"
    elif(sql.find("CREATE TABLE") == 0):
        return "CREATE TABLE"
    elif(sql.find("UPDATE") == 0):
        return "UPDATE"
    else:
        return "OTHER"

def getInfo_create(sql : str) -> str:
    """테이블 이름을 반환합니다."""
    sql = string_module.removeNoise(sql)
    tableName = string_module.getParenthesesContext2(sql, "CREATE TABLE ", "(")
    tableName = string_module.removeEndNoise(tableName)
    return tableName

def getInfo_insert(sql : str, tableInfo : table_info_module.TableInfo) -> tuple:
    """테이블 이름과 컬럼을 반환합니다."""
    sql = string_module.removeNoise(sql)
    tableName = string_module.getParenthesesContext2(sql, "INSERT INTO ", " ")
    columns = tableInfo[tableName]
    return (tableName, columns)

def getInfo_update(sql : str, tableInfo : table_info_module.TableInfo) -> tuple:
    """테이블 이름과 컬럼, where 조건문을 반환합니다"""
    sql = string_module.removeNoise(sql)
    tableName = string_module.getParenthesesContext2(sql, "UPDATE ", " ")
    columns = tableInfo[tableName]
    start = sql.find("WHERE")
    where = "1"
    if(start > -1):
        where = sql[start + len("WHERE") :]
    return (tableName, columns, where)

    
