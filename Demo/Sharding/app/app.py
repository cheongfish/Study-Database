from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncpg
import hashlib
import base64
from utils.hashring import HashRing

app = FastAPI()

shards = ["shard1", "shard2", "shard3"]
ring = HashRing(shards)
clients = {}

async def connect():
    global clients
    clients["shard1"] = await asyncpg.connect(
        host="postgres-shard1.postgres.svc.cluster.local",
        port=5432,
        user="user",
        password="password",
        database="postgres"
    )
    clients["shard2"] = await asyncpg.connect(
        host="postgres-shard2.postgres.svc.cluster.local",
        port=5432,
        user="user",
        password="password",
        database="postgres"
    )
    clients["shard3"] = await asyncpg.connect(
        host="postgres-shard3.postgres.svc.cluster.local",
        port=5432,
        user="user",
        password="password",
        database="postgres"
    )

@app.on_event("startup")
async def startup_event():
    await connect()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

@app.post("/")
async def hash_url(request: Request):
    url = request.query_params.get("url")
    if not url:
        return {"error": "Missing 'url' query parameter"}

    hash_bytes = hashlib.sha256(url.encode()).digest()
    hash_base64 = base64.b64encode(hash_bytes).decode()
    shard = ring.get_node(url)

    return {
        "hash": hash_base64,
        "shard": shard
    }