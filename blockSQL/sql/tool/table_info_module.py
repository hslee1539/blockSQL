import sqlite3

class TableInfo:
    table_dic = {}
    cursor : sqlite3.Cursor

    def __init__(self, cursor : sqlite3.Cursor):
        self.cursor = cursor

    def __getitem__(self, key : str) -> str:
        try:
            retval = self.table_dic[key]
        except KeyError:
            # 없으므로, 찾아 추가함.
            tmp = self.cursor.execute("""
            PRAGMA table_info({0})""".format(key)).fetchall()
            retval = tmp[0][1]
            for i in range(1,len(tmp)):
                retval += "," + tmp[i][1]
            self.table_dic[key] = retval
        return retval