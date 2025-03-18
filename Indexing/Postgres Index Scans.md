# PostgreSQL 인덱스 스캔

## 1. 개요
PostgreSQL에서 데이터를 검색할 때 사용할 수 있는 다양한 스캔 방식이 있습니다. 이번 글에서는 다음과 같은 스캔 방식을 설명합니다.

- **순차 테이블 스캔 (Sequential Table Scan)**
- **인덱스 스캔 (Index Scan)**
- **비트맵 인덱스 스캔 (Bitmap Index Scan)**

이제 각 스캔 방식이 어떻게 동작하는지 자세히 살펴보겠습니다.

---

## 2. 데이터베이스 테이블 구성
다음과 같은 "Grades" 테이블을 사용하여 설명합니다.

```sql
CREATE TABLE grades (
    ID SERIAL PRIMARY KEY,
    name TEXT,
    grade INT
);
CREATE INDEX idx_grade ON grades(grade);
```

- `ID`: 기본 키(Primary Key)이며 자동 증가합니다.
- `name`: 학생의 이름 (인덱스 없음)
- `grade`: 학생의 점수 (0~100 범위)이며, 인덱스가 존재함.

이제 각 스캔 방식의 동작을 살펴보겠습니다.

---

## 3. 인덱스 스캔 (Index Scan)
```sql
EXPLAIN SELECT name FROM grades WHERE ID = 1000;
```

- PostgreSQL은 기본 키 인덱스를 사용하여 `ID = 1000`을 찾음.
- 해당 `ID`가 존재하는지 확인한 후, 테이블에서 `name` 값을 가져옴.
- **이 과정에서 인덱스에 없는 컬럼(`name`)은 테이블에서 가져와야 하므로 추가적인 랜덤 접근(Random Access)이 발생함).**

### 3.1 랜덤 접근(Random Access)의 문제
```sql
EXPLAIN SELECT name FROM grades WHERE ID < 100;
```

- 인덱스를 통해 1부터 99까지의 ID를 찾은 후, 개별적으로 테이블을 조회.
- **각 행을 가져올 때마다 테이블을 조회해야 하므로 성능이 저하될 수 있음.**

---

## 4. 순차 테이블 스캔 (Sequential Table Scan)
```sql
EXPLAIN SELECT name FROM grades WHERE ID > 100;
```

- 데이터가 많을 경우(예: 5천만 개 중 500만 개 조회), PostgreSQL은 **순차 테이블 스캔(Sequential Scan)**을 선택함.
- **인덱스를 사용하는 것보다 전체 테이블을 읽는 것이 더 빠르다고 판단됨.**

---

## 5. 비트맵 인덱스 스캔 (Bitmap Index Scan)
```sql
EXPLAIN SELECT name FROM grades WHERE grade > 95;
```

- **비트맵(Bitmap) 구조를 활용하여 여러 페이지를 한 번에 가져옴.**
- 개별 행을 조회하는 랜덤 접근보다 효율적이며, 중간 규모의 데이터 조회에 적합.

### 5.1 비트맵 인덱스 스캔의 응용
```sql
EXPLAIN SELECT name FROM grades WHERE grade > 95 AND ID < 10000;
```

- `grade`와 `ID` 컬럼에 각각 인덱스가 존재할 경우,
  - `grade` 인덱스로 비트맵 생성
  - `ID` 인덱스로 비트맵 생성
  - 두 비트맵을 **AND 연산**하여 필요 없는 페이지를 제거함.
- **결과적으로 불필요한 테이블 접근을 줄여 성능 최적화 가능.**

---

## 6. 결론
| 스캔 방식 | 특징 |
|-----------|------|
| 순차 테이블 스캔 | 테이블 전체를 읽음. 데이터가 많을 때 비효율적일 수 있음. |
| 인덱스 스캔 | 인덱스를 통해 데이터 검색. 랜덤 접근이 많으면 성능 저하 가능. |
| 비트맵 인덱스 스캔 | 중간 규모의 데이터에 적합. 여러 인덱스를 결합하여 효율적으로 조회 가능. |
