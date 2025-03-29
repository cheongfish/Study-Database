const app = require("express")();
const { Client } = require("pg");
const crypto = require("crypto")
const ConsisentHash = require("consistent-hash");
const hr = new ConsisentHash();
hr.add("shard1")
hr.add("shard2")
hr.add("shard3")

const clients = {
    "shard1": new Client({
        "host": "postgres-shard1",
        "port": "5432",
        "user": "user",
        "password": "password",
        "database": "postgres"
    }),
    "shard2": new Client({
        "host": "postgres-shard2",
        "port": "5432",
        "user": "user",
        "password": "password",
        "database": "postgres"
    }),
    "shard3": new Client({
        "host": "postgres-shard3",
        "port": "5432",
        "user": "user",
        "password": "password",
        "database": "postgres"
    }),

}

connect();
async function connect() {
    await clients["shard1"].connect();
    await clients["shard2"].connect();
    await clients["shard3"].connect();
}


app.get("/", (req, res) => {

})

app.post("/", (req, res) => {

    const url = req.query.url;
    //www.wikipedia.com/sharding
    // consistently hash this to get a port!
    const hash = crypto.createHash("sha256").update(url).digest("base64")

    res.send({
        "hash": hash
    })
})

app.listen(8081, () => console.log("Listening 8081"))