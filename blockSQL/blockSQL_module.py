#from blockSQL.tool import Text, SpaceStr
import time
import hashlib

sha256 = hashlib.sha256()

class BlockSQL:
    mergeTimeMax = 99999999999.0
    __selectBranch : str
    __selectMerge : str
    __loginTime : float

    def __init__(self):
        pass
    def login(self, loginTime = time.time()):
        self.loginTime = loginTime

    @property
    def loginTime(self):
        return self.__loginTime
    @loginTime.setter
    def loginTime(self, value):
        self.__loginTime = value
        self.__selectBranch = "\
SELECT loginTime, sqlTime, sql, json, branchHash \
FROM block \
WHERE mergeTime = (\
    SELECT MAX(mergeTime) \
    FROM block \
    WHERE mergeTime != {1}\
) OR \
    mergeTime = {1} \
    AND loginTime = {0} \
ORDER BY mergeTime, sqlTime".format(str(self.__loginTime), str(self.mergeTimeMax))

        self.__selectMerge = "\
SELECT * \
FROM block \
WHERE {0} = (\
        SELECT MIN(loginTime) \
        FROM block \
        WHERE mergeTime = {1} \
    ) AND (\
        mergeTime = (\
            SELECT MAX(mergeTime) \
            FROM block \
            WHERE mergeTime != {1} \
        ) OR mergeTime = {1}\
    )\
ORDER BY mergeTime, sqlTime\
;".format(str(self.__loginTime), str(self.mergeTimeMax))
    
    def create(self, sqlTime = time.time())->tuple:
        return "\
CREATE TABLE block (\
    loginTime REAL NOT NULL, \
    sqlTime REAL NOT NULL, \
    mergeTime REAL, \
    sql TEXT, \
    json TEXT, \
    branchHash TEXT, \
    mergeHash TEXT, \
    PRIMARY KEY(loginTime, sqlTime)\
);","\
INSERT INTO block(\
    loginTime,\
    sqlTime,\
    mergeTime,\
    branchHash,\
    mergeHash\
) VALUES(\
    0.0,\
    0.0,\
    0.0,\
    'no-hash',\
    'no-hash'\
);"
    def isCreate(self) -> str:
        return "SELECT name FROM sqlite_master WHERE type='table' and name='block';"
    def insert(self, sql : str, json : str, sqlTime = time.time())->str:
        return "\
INSERT INTO block (loginTime, sqlTime, mergeTime, sql, json) \
VALUES ({0}, {1}, {4},'{2}', '{3}')".format(self.__loginTime, sqlTime, sql, json, self.mergeTimeMax)

    def selectBranch(self)->str:
        """최근에 병합이 완료된 블록과 자신이 만든 분기를 sqlTime 순으로 select 합니다.\n\
fetch 시, loginTime, sqlTime, sql, json, branchHash를 반환합니다."""
        return self.__selectBranch
    def selectMerge(self) -> str:
        return self.__selectMerge
    @staticmethod
    def createBranchHash(loginTime : float, sqlTime : float, sql : str, json : str, branchHash : str) -> str:
        tmp = "block1" +str(loginTime) + str(sqlTime) + str(sql) + str(json) + str(branchHash)
        sha256.update(tmp.encode())
        return sha256.hexdigest()
    @staticmethod
    def createMergeHash(loginTime : float, sqlTime : float, mergeTime : float, sql : str, json : str, branchHash : str, mergeHash : str) -> str:
        tmp = "block2" + str(loginTime) + str(sqlTime) + str(mergeTime) + str(sql) + str(json) + str(branchHash) + str(mergeHash)
        sha256.update(tmp.encode())
        return sha256.hexdigest()
    @staticmethod
    def updateBranch(loginTime : float, sqlTime : float, branchHash : str) -> str:
        return "UPDATE block SET branchHash = '{2}' WHERE loginTime = {0} AND sqlTime = {1}".format(loginTime, sqlTime, branchHash)

    @staticmethod
    def updateMerge(loginTime : float, sqlTime : float, mergeTime : float, mergeHash : str) -> str:
        return "UPDATE block SET mergeTime = {2}, mergeHash = '{3}' WHERE loginTime = {0} AND sqlTime = {1}".format(loginTime, sqlTime, mergeTime, mergeHash)

    


# 참고 1
#
# 1.    가장 sqlTime이 높은 loginTime을 찾는다.
# 1.1.  만약 다수면, loginTime이 가장 큰 값을 기준으로 한다.
#
# 2.    1. 에서 찾은 loginTime에서 모든 널값을 select 한다.
# 
# 3.    select된 널값들 중에 가장 sqlTime이 높은 것을 해쉬 적용한다.
#
# 4.    2.를 반복한다.

#   where sqlTime = (
#       select max(sqlTime)
#       from block
#       where private = null
#           and loginTime = (
#               select max(loginTime)
#               from block
#               where sqlTime = (
#                   select max(sqlTime)
#                   from block
#               )
#           )
#       )
# 
