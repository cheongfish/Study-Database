# SQL OFFSET을 사용하지 말아야 하는 이유

## 🧩 OFFSET이란?

OFFSET은 SQL에서 페이징 시 특정 수의 행을 건너뛰고 이후의 행을 가져오도록 합니다.

예시:
```sql
SELECT title FROM news ORDER BY id DESC OFFSET 100 LIMIT 10;
```

위 쿼리는 100개의 행을 건너뛰고 다음 10개를 가져옵니다.

## 🐢 OFFSET의 성능 문제

- OFFSET은 내부적으로 **건너뛰는 행도 모두 조회**합니다.
- OFFSET이 커질수록 데이터베이스는 **더 많은 행을 불필요하게 처리**하게 됩니다.
- 100만번째 페이지를 조회할 경우, 백만 개가 넘는 행을 가져와 일부만 반환 → 비효율적!
- 실시간 데이터 추가 시 **중복 레코드**가 발생할 수 있어 정확한 페이징이 어려움

## 🧪 Postgres에서 실험 결과

- OFFSET 0 → 매우 빠름 (0.2ms)
- OFFSET 1,000 → 1ms
- OFFSET 100,000 → 79ms
- OFFSET 1,000,000 → 수 초 이상

이는 **인덱스 역방향 스캔**에도 불구하고 OFFSET이 증가함에 따라 처리량이 급증함을 보여줍니다.

## ✅ 성능을 높이는 대안: 커서 기반 페이징

OFFSET 대신 **마지막으로 조회한 ID**를 기준으로 다음 페이지를 조회합니다.

```sql
-- 첫 페이지 조회
SELECT id, title FROM news ORDER BY id DESC LIMIT 10;

-- 이후 페이지 조회
SELECT id, title FROM news WHERE id < 마지막_조회_ID ORDER BY id DESC LIMIT 10;
```

### 장점
- 인덱스를 직접 활용해 **빠른 조회**
- **건너뛰는 작업 없음** → 처리 성능 향상
- **중복 또는 누락 방지** → 안정적인 페이징

## 📌 결론

- OFFSET 기반 페이징은 간단하지만 성능이 나쁩니다.
- 커서 기반 페이징은 조금 더 복잡하지만 훨씬 효율적입니다.
- 특히 대용량 데이터셋에서는 커서 기반 방식이 필수적입니다.

## 📚 참고 리소스

- [Use the Index, Luke!](https://use-the-index-luke.com)