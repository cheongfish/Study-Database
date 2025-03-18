# Postgres에서 EXPLAIN 사용법

## 1. EXPLAIN 개요

Postgres에는 `EXPLAIN`이라는 명령어가 있으며, 이는 특정 SQL 문에 대해 Postgres가 어떤 실행 계획을 사용할 것인지 정보를 제공하는 기능입니다.

## 2. 예제 테이블 소개

실습을 위해 `grades` 테이블을 사용합니다. 이 테이블에는 학생들의 성적 데이터가 저장되어 있으며, 다음과 같은 필드를 포함하고 있습니다.

- `ID`: 정수형, 기본 키, 인덱스 존재
- `grade`: 정수형, 인덱스 존재
- `name`: 문자열, 인덱스 없음

테이블에는 약 2억 개 이상의 행이 존재합니다.

## 3. 기본적인 EXPLAIN 실행

### 3.1 `SELECT *` 실행 시 실행 계획 확인

```sql
EXPLAIN SELECT * FROM grades;
```

이 경우, Postgres는 **순차 검색(Sequential Scan)** 을 수행합니다. 이는 다른 데이터베이스에서 **풀 테이블 스캔(Full Table Scan)** 이라고 불리는 방식과 유사합니다. 테이블 전체를 읽어야 하므로 성능이 저하될 수 있습니다.

## 4. EXPLAIN 결과 분석

Postgres에서 `EXPLAIN` 결과에는 다음과 같은 `cost` 값이 표시됩니다:

```
Seq Scan on grades  (cost=0.00..289000.00 rows=200000000 width=31)
```

- 첫 번째 `cost` 값(`0.00`): 첫 번째 페이지를 가져오는 데 필요한 예상 비용
- 두 번째 `cost` 값(`289000.00`): 전체 쿼리 실행 비용

이 값은 상대적인 비용을 의미하며, 실제 실행 시간을 의미하지 않습니다.

## 5. ORDER BY가 포함된 쿼리 실행

### 5.1 인덱스를 활용한 정렬

```sql
EXPLAIN SELECT * FROM grades ORDER BY grade;
```

- `grade` 컬럼에 인덱스가 존재하므로 **인덱스를 이용한 정렬(Index Scan)** 이 수행됩니다.

### 5.2 인덱스가 없는 컬럼 정렬 문제

```sql
EXPLAIN SELECT * FROM grades ORDER BY name;
```

- `name` 컬럼에는 인덱스가 없으므로 **병렬 순차 검색(Parallel Sequential Scan) 후 정렬(Sort)** 이 수행됩니다.
- 실행 시간이 크게 증가할 수 있습니다.

## 6. 특정 컬럼만 선택하는 경우

```sql
EXPLAIN SELECT ID FROM grades;
```

- `ID` 필드는 정수형(4바이트)이므로 `width=4`
- `name` 필드는 가변 길이 문자열이므로 평균적으로 `width=19`
- `SELECT *`를 수행하면 네트워크 대역폭 사용량이 증가할 수 있으므로 주의가 필요합니다.

## 7. 인덱스를 활용한 조회

### 7.1 기본적인 인덱스 검색

```sql
EXPLAIN SELECT * FROM grades WHERE ID = 10;
```

- `ID`는 기본 키이므로 **인덱스 검색(Index Scan)** 수행
- 인덱스를 통해 데이터 위치를 찾은 후 **힙(Heap)에서 실제 데이터 조회**

### 7.2 인덱스 전용 검색

```sql
EXPLAIN SELECT ID FROM grades WHERE ID = 10;
```

- `ID`만 조회하는 경우 **인덱스 전용 검색(Index Only Scan)** 이 수행될 수 있음
- 힙 접근 없이 인덱스에서 직접 데이터 반환 가능 → 성능 향상

## 8. SELECT COUNT(\*) 대신 EXPLAIN 활용

```sql
SELECT COUNT(*) FROM grades;
```

- 행 개수를 직접 세는 `COUNT(*)`는 성능을 크게 저하시킬 수 있음
- 대신 `EXPLAIN`을 사용하여 **통계적 추정치** 를 활용하면 더 효율적

## 9. 결론

- `EXPLAIN`을 활용하면 쿼리 실행 계획을 예측할 수 있음
- `Sequential Scan`은 테이블 전체를 읽어야 하므로 성능이 저하될 수 있음
- `Index Scan`과 `Index Only Scan`을 활용하면 검색 속도를 개선할 수 있음
- `ORDER BY` 시, 인덱스가 없는 컬럼을 정렬하면 성능이 저하될 수 있음
- `SELECT COUNT(*)` 대신 `EXPLAIN`을 활용하여 효율적인 데이터 조회 가능

이번 강의에서는 `EXPLAIN` 명령어를 활용한 실행 계획 분석 방법을 설명하였습니다. 다음 강의에서는 `EXPLAIN ANALYZE`를 사용하여 실제 실행 시간을 분석하는 방법을 다뤄보겠습니다!

