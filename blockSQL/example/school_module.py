import sys
import os
sys.path.append(os.path.dirname(__file__) + "\..\..")

import blockSQL

connection = blockSQL.Connection(":memory:")
connection.execute("""
CREATE TABLE stu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
);
""")
connection.execute("""
CREATE TABLE tea(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    class TEXT,
    age INTEGER
)
""")



connection.execute("""
INSERT INTO stu
VALUES(
    1,
    "이희수",
    14
)
""")
print("stu table : ", connection.execute("""
SELECT *
FROM stu
""").fetchall())
print("tea table : ", connection.execute("""
SELECT *
FROM tea
""").fetchall())
print("stu_history table : ", connection.execute("""
SELECT *
FROM stu_history
""").fetchall())
print("tea_history table : ", connection.execute("""
SELECT *
FROM tea_history
""").fetchall())
print("block table : ", connection.execute("""
SELECT *
FROM block
""").fetchall())



connection.execute("""
INSERT INTO stu (name, age)
VALUES(
    "홍길동",
    12
)
""")
print("stu table : ", connection.execute("""
SELECT *
FROM stu
""").fetchall())
print("tea table : ", connection.execute("""
SELECT *
FROM tea
""").fetchall())
print("stu_history table : ", connection.execute("""
SELECT *
FROM stu_history
""").fetchall())
print("tea_history table : ", connection.execute("""
SELECT *
FROM tea_history
""").fetchall())
print("block table : ", connection.execute("""
SELECT *
FROM block
""").fetchall())


connection.execute("""
UPDATE stu
SET age = 13
WHERE name = "홍길동"
""")
print("stu table : ", connection.execute("""
SELECT *
FROM stu
""").fetchall())
print("tea table : ", connection.execute("""
SELECT *
FROM tea
""").fetchall())
print("stu_history table : ", connection.execute("""
SELECT *
FROM stu_history
""").fetchall())
print("tea_history table : ", connection.execute("""
SELECT *
FROM tea_history
""").fetchall())
print("block table : ", connection.execute("""
SELECT *
FROM block
""").fetchall())
