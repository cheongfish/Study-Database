# 데이터베이스에서의 인덱싱

## 1. 인덱스란?
* 인덱스는 기존 테이블 위에 구축되고 할당되는 데이터 구조

### 인덱스의 개념적 이해
* 전화번호부를 통해 특정한 이름을 찾을때 빠르게 검색할 수 있음
* 같은 원리로 데이터를 검색할 때 효율적으로 접근할 수 있도록 도와줌


## 2. 인덱스의 종류
- **B-트리(B-Tree) 인덱스**: 
  * 일반적으로 관계형 데이터베이스에서 사용되며, 검색을 효율적으로 수행할 수 있도록 균형 트리 구조를 유지함
- **LSM-트리(LSM-Tree) 인덱스**:
  *  쓰기 작업이 많은 환경에서 성능을 최적화하기 위해 설계된 트리 구조

## 3. 실습 - 인덱스 성능 비교
### 3.1 실험 환경
테스트 테이블: `employees`
- 약 1,100만 개의 행 보유
- `ID` 필드: 정수형, NULL 불가, 자동 증가, 기본 키 설정
- `name` 필드: 단순 문자열 저장, 인덱스 없음

### 3.2 기본 키(Primary Key) 조회 성능
```sql
SELECT ID FROM employees WHERE ID = 1000;
```
이 경우, `ID`는 기본 키이므로 자동으로 생성된 B-트리 인덱스를 활용하여 빠르게 검색됩니다.

### 3.3 `EXPLAIN ANALYZE`를 이용한 실행 계획 분석
```sql
EXPLAIN ANALYZE SELECT ID FROM employees WHERE ID = 2000;
```
- 결과: 인덱스를 사용하여 매우 빠르게 검색 (약 0.6ms)
- B-트리는 범위를 좁혀가며 데이터를 빠르게 찾음

### 3.4 인덱스가 없는 필드 조회 성능
```sql
EXPLAIN ANALYZE SELECT name FROM employees WHERE ID = 5000;
```
- `ID`는 인덱스를 활용하여 빠르게 찾을 수 있지만, `name` 필드는 별도의 인덱스가 없기 때문에 추가적인 디스크 접근이 필요
- 실행 시간: 2.5ms (약간 증가)

### 3.5 인덱스가 없는 필드에서 조건 검색
```sql
EXPLAIN ANALYZE SELECT ID FROM employees WHERE name = 'XZ';
```
- `name` 필드에 인덱스가 없으므로 테이블 전체를 순차 검색(Sequential Scan)
- 실행 시간: 3초 이상 (매우 느림)

## 4. 해결책 - 인덱스 추가
```sql
CREATE INDEX employees_name_idx ON employees(name);
```
인덱스 추가 후 동일한 조회 쿼리를 실행해 보면 실행 속도가 크게 개선됩니다.

```sql
EXPLAIN ANALYZE SELECT ID FROM employees WHERE name = 'XZ';
```
- 실행 시간: 47ms (대폭 감소)
- 테이블 전체를 검색하지 않고 인덱스를 활용하여 빠르게 조회 가능

### 4.1 인덱스 사용이 어려운 경우
```sql
EXPLAIN ANALYZE SELECT ID FROM employees WHERE name LIKE '%XZ%';
```
- 와일드카드(`%`)가 앞에 포함된 경우, 인덱스를 활용할 수 없음
- 실행 시간 증가 (인덱스를 사용하지 못하고 전체 검색 수행)

## 5. 결론
1. **기본 키(Primary Key)**는 자동으로 인덱스를 가짐
2. **인덱스가 없으면 전체 테이블 검색(Sequential Scan)으로 인해 성능 저하**
3. **모든 경우에 인덱스가 사용되는 것은 아님** (실행 계획을 분석하는 것이 중요)
4. **문자열 검색 시 `LIKE '%값%'` 사용에 주의** (인덱스가 활용되지 않음)
