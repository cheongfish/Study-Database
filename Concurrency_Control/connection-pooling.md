### 📘 Database Connection Pooling 

#### 🔗 연결 풀링이란?
- **연결 풀링(Connection Pooling)**: TCP 연결을 재사용하여, 매 요청마다 연결을 새로 열고 닫는 비용을 줄이는 기술.
- **장점**:
  - 연결 설정 및 해제의 비용 절감
  - 제한된 DB 연결 수의 효율적 사용
  - 많은 클라이언트 환경에서 성능 향상

---

#### 🆚 전통적인 방식 vs 풀링 방식

| 항목 | 전통 방식 (`Client`) | 풀링 방식 (`Pool`) |
|------|----------------------|---------------------|
| 연결 시점 | 매 요청마다 연결 생성 및 해제 | 애플리케이션 시작 시 풀 생성 |
| 성능 | 느림 (비용 많이 듦) | 빠름 (재사용 가능) |
| 상태 관리 | 무상태 | 반유지 상태 가능 |
| 사용 예 | 간단한 요청 | 고빈도 요청, 트랜잭션 처리 |

---

#### ⚙️ Node.js 설정 비교

##### 기존 방식
```js
const client = new Client(config);
await client.connect();
const result = await client.query("SELECT * FROM employees");
await client.end();
```

##### 풀링 방식
```js
const pool = new Pool({ max: 20, idleTimeoutMillis: 10000, connectionTimeoutMillis: 2000 });
const result = await pool.query("SELECT * FROM employees");
```

- **max**: 최대 연결 수
- **idleTimeoutMillis**: 사용되지 않는 연결을 종료하는 시간
- **connectionTimeoutMillis**: 연결 대기 시간

---

#### ⏱ 성능 테스트

- `/old`: 기존 방식, 1000번 요청 평균 40ms
- `/pool`: 풀 방식, 1000번 요청 평균 19ms
- **약 50% 향상**, 클라우드 환경에서는 더 큰 차이 발생

---

#### 🔁 고급 사용법 (트랜잭션 등)
- 클라이언트를 풀에서 가져와 직접 사용 가능:
```js
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('...');
  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
} finally {
  client.release();
}
```

---

### ✅ 결론
- 연결 풀링은 고성능 서버 구축에 필수
- Node.js 환경에서 `pg`의 `Pool`을 적극 활용
- 트랜잭션이 필요한 경우 클라이언트를 직접 관리 가능
