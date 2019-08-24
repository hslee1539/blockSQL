blockSQL
======
# index
1. [소개](#1.소개)

2. [설치](#2.설치)

3. [예제](#3.예제)

    3.1. [학교](#3.1.학교)

4. [모듈 설명](#4.모듈-설명)


# 1.소개

 하나의 데이터베이스안 모든 테이블의 모든 연산에 대해, 각각의 테이블에 대한 history와 그 모든 history에 대한 블록체인을 관리하는 패키지입니다.

![구조설명](./doc/구조.png)

 위 그림에서 사용자는 A,B 테이블을 만들고 sql명령어로 A,B 테이블 연산을 하면 blockSQL이 자동으로 A_history와 B_history 그리고 block chain 테이블을 관리합니다.

 ![구조설명2](./doc/block-history-구조.png)

A_history 테이블은 history id와 추가로 A 테이블의 컬럼을 그대로 가지고 있어, 빠르게 특정 기록을 검색할 수 있습니다.

그리고 block table은 block chain 구조이고, history의 내용과 이전 블록의 row를 해시한 결과를 가집니다. 각각 사용자가 만든 모든 테이블에 대한 각각의 history는 컬럼이 다르기 때문에 텍스트화 해서 저장합니다. 또 저장을 RC4 알고리즘으로 해당 블록의 해시값을 키로 사용해서 암호화 해서 저장합니다.

# 2.설치

[blockSQL.zip](https://github.com/hslee1539/blockSQL/archive/master.zip)

또는

`git clone https://github.com/hslee1539/blockSQL.git`으로 작업 폴더에 blockSQL 폴더가 있으면 됩니다.

# 3.예제
## 3.1.학교
[school_module.py](./example/school_module.py)


# 4.모듈 설명
