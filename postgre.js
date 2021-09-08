const { Pool, Client } = require("pg");
let _db = null;
let connection;


const credentials = {
    user: "Bryann",
    host: "localhost",
    database: "grove",
    password: "grove123",
    port: 5432,
};

function connect() {
    const pool = new Pool(credentials)
    _db = pool
    if (_db !== null) {
        return Promise.resolve(_db)
    }
}

module.exports = {
    connect,
    connection: { db: () => _db }
}

