import sqlite3
import hashlib
import time
import blockSQL

def execute(cursor : sqlite3.Cursor, sql : str, tableInfo : blockSQL.sql.tool.table_info_module.TableInfo, hashFunc = hashlib.sha256, timeFunc = time.time) -> sqlite3.Cursor:
    sql = blockSQL.sql.sql_module.string_module.removeHeadNoise(sql)
    sql = blockSQL.sql.sql_module.string_module.removeHeadNoise(sql, '\n')
    sql = blockSQL.sql.sql_module.string_module.removeHeadNoise(sql)
    funcName = blockSQL.sql.sql_module.findFunc(sql)
    if(funcName == "CREATE TABLE"):
        tableName = blockSQL.sql.sql_module.getInfo_create(sql)
        blockSQL.sql.currentTable_module.create(cursor, sql, tableName)
        blockSQL.sql.historyTable_module.create(cursor, tableName)
    elif(funcName == "INSERT INTO"):
        tableName, columns = blockSQL.sql.sql_module.getInfo_insert(sql, tableInfo)
        blockSQL.sql.currentTable_module.insert(cursor, sql, tableName)
        blockSQL.sql.historyTable_module.insert(cursor, tableName, columns, timeFunc)
        blockSQL.sql.block_module.insert(cursor, tableName, hashFunc, timeFunc)
        blockSQL.sql.currentTable_module.done(cursor, tableName)
    elif(funcName == "UPDATE"):
        tableName, columns, where = blockSQL.sql.sql_module.getInfo_update(sql, tableInfo)
        blockSQL.sql.currentTable_module.update(cursor, tableName, where, sql)
        blockSQL.sql.historyTable_module.insert(cursor, tableName, columns, timeFunc)
        blockSQL.sql.block_module.insert(cursor, tableName, hashFunc, timeFunc)
        blockSQL.sql.currentTable_module.done(cursor, tableName)
    else:
        return cursor.execute(sql)
    return cursor