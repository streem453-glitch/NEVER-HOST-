import { createServer } from "node:http";
import { randomUUID } from "node:crypto";
import { Sandbox } from "railway";

const PORT = Number(process.env.PORT || 3000);
const API_KEY = process.env.EXECUTOR_API_KEY;

const bots = new Map();

const server = createServer(async (req, res) => {
res.setHeader("Content-Type", "application/json; charset=utf-8");

if (req.url === "/health" && req.method === "GET") {
res.writeHead(200);
return res.end(JSON.stringify({ status: "ok" }));
}

if (!API_KEY || req.headers.authorization !== "Bearer ${API_KEY}") {
res.writeHead(401);
return res.end(JSON.stringify({ error: "Unauthorized" }));
}

if (req.method !== "POST" || req.url !== "/sandboxes") {
res.writeHead(404);
return res.end(JSON.stringify({ error: "Not found" }));
}

// Пока не запускаем загруженный код:
// сначала проверим защищённое соединение.
res.writeHead(501);
res.end(JSON.stringify({
error: "Sandbox запуск ещё не включён"
}));
});

server.listen(PORT, "0.0.0.0", () => {
console.log("Executor listening on port ${PORT}");
});
