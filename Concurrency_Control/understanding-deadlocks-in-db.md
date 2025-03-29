## 🔒 데드락(Deadlock)이란?

- **정의**: 두 개 이상의 트랜잭션이 서로가 보유한 리소스를 기다리며 무한 대기 상태에 빠지는 현상
- **발생 예시**:
  - 트랜잭션 1이 `id = 20`을 점유한 상태에서 `id = 21`을 요청
  - 트랜잭션 2가 `id = 21`을 점유한 상태에서 `id = 20`을 요청
  - → **서로 대기 상태 → 데드락 발생**
- **PostgreSQL의 동작**: 자동으로 데드락을 감지하고, 일반적으로 **마지막에 진입한 트랜잭션을 롤백**

---

## ✅ 데드락 실습 예제 (PostgreSQL)

```sql
-- 테이블 생성
CREATE TABLE test (
  id INT PRIMARY KEY,
  value TEXT
);

-- 트랜잭션 1
BEGIN;
INSERT INTO test (id, value) VALUES (20, 'T1');

-- 트랜잭션 2 (다른 세션)
BEGIN;
INSERT INTO test (id, value) VALUES (21, 'T2');

-- 트랜잭션 1에서 21을 삽입 시도 → 대기
INSERT INTO test (id, value) VALUES (21, 'T1 again');

-- 트랜잭션 2에서 20을 삽입 시도 → 데드락 발생
INSERT INTO test (id, value) VALUES (20, 'T2 again');
```

---

## 💡 낙관적 시나리오 (데드락 없이 처리)

- 트랜잭션 1: 20 삽입 후 `ROLLBACK`
- 트랜잭션 2: 이후 동일 값 삽입 → **성공**

---

## ❗ 중복 키 오류 예시

- 트랜잭션 2에서 먼저 커밋한 후
- 트랜잭션 1이 동일 키 삽입 → **중복 키 에러 발생**

---

## 🔐 2단계 잠금(2PL: Two-Phase Locking)

### 개념
- **1단계(확장 단계)**: 잠금 획득만 가능
- **2단계(축소 단계)**: 잠금 해제만 가능
- 한 번 해제한 잠금은 다시 획득할 수 없음

### 예시: 좌석 예약 시스템의 이중 예약 방지

```sql
-- 테이블 예시
CREATE TABLE seats (
  id INT PRIMARY KEY,
  reserved BOOLEAN DEFAULT FALSE,
  reserved_by TEXT
);

-- 트랜잭션 1
BEGIN;
SELECT * FROM seats WHERE id = 14 FOR UPDATE;
UPDATE seats SET reserved = TRUE, reserved_by = '후세인' WHERE id = 14;
COMMIT;

-- 트랜잭션 2 (동일 시도)
BEGIN;
SELECT * FROM seats WHERE id = 14 FOR UPDATE;
-- 대기 상태 (배타 락 때문에)
```

- 트랜잭션 1이 **배타 락을 먼저 획득**하고 커밋
- 트랜잭션 2는 대기하다가 **락 해제 후에 실행되거나 실패 처리**

---

## 🧠 핵심 요약

| 항목 | 설명 |
|------|------|
| 데드락 | 서로 잠긴 리소스를 기다리는 무한 대기 상태 |
| PostgreSQL 처리 | 데드락 감지 후 자동 롤백 |
| 2PL | 트랜잭션 중간에 잠금 해제를 허용하지 않는 규칙 |
| 실습 예시 | 좌석 예약, 중복 키 삽입 등 |

---

