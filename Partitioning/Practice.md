---

## 🎓 Postgres 파티셔닝 실습 (Demo with Docker)

---

### 🐳 1. Docker로 Postgres 실행

```bash
docker run -d \
  --name pgmain \
  -e POSTGRES_PASSWORD=yourpassword \
  postgres
```

컨테이너 접속 및 Postgres 진입:

```bash
docker exec -it pgmain bash
psql -U postgres
```

---

### 🏗️ 2. 원본 테이블 생성 (`grades_org`)

```sql
CREATE TABLE grades_org (
  id serial NOT NULL,
  g int NOT NULL
);
```

---

### 📥 3. 데이터 삽입 (1천만 행)

```sql
INSERT INTO grades_org (g)
SELECT floor(random() * 100)::int
FROM generate_series(1, 10000000);
```

---

### 🔍 4. 인덱스 생성

```sql
CREATE INDEX grades_org_index ON grades_org (g);
```

---

### 📜 5. 테이블 구조 확인

```sql
\d grades_org
```

---

## 🧩 다음 단계: 파티셔닝 실습

---

### 🗂️ 6. 파티셔닝 마스터 테이블 생성

```sql
CREATE TABLE grades (
  id serial NOT NULL,
  g int NOT NULL
) PARTITION BY RANGE (g);
```

---

### 📁 7. 파티션 테이블 생성 (예: 성적 구간별)

```sql
CREATE TABLE grades_0_20 PARTITION OF grades
  FOR VALUES FROM (0) TO (21);

CREATE TABLE grades_21_40 PARTITION OF grades
  FOR VALUES FROM (21) TO (41);

CREATE TABLE grades_41_60 PARTITION OF grades
  FOR VALUES FROM (41) TO (61);

CREATE TABLE grades_61_80 PARTITION OF grades
  FOR VALUES FROM (61) TO (81);

CREATE TABLE grades_81_100 PARTITION OF grades
  FOR VALUES FROM (81) TO (101);
```

---

### 🚚 8. 데이터 이관 (기존 테이블 → 파티션 테이블)

```sql
INSERT INTO grades (g)
SELECT g FROM grades_org;
```

---

### ⚡ 9. 쿼리 테스트 및 성능 비교

예: 특정 성적대만 조회

```sql
EXPLAIN ANALYZE
SELECT * FROM grades WHERE g BETWEEN 41 AND 60;
```

---
