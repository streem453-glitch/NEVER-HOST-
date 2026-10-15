
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="NEVER-HOST")

@app.get("/")
def home():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>NEVER-HOST♥️</title>
      <style>
        body {
          background:#101014; color:#fff; font-family:Arial,sans-serif;
          max-width:650px; margin:50px auto; padding:20px;
        }
        .card { background:#1c1c25; padding:22px; border-radius:16px; }
        h1 { color:#c084fc; }
        p { line-height:1.6; }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>NEVER-HOST♥️</h1>
        <p>Сервер работает!</p>
        <p>Это первый настоящий этап подключения.</p>
        <p>Панель управления ботами добавим следующим шагом.</p>
        <p><a href="/health" style="color:#c084fc">Проверить состояние API</a></p>
      </div>
    </body>
    </html>
    """)

@app.get("/health")
def health():
    return {"status": "ok", "service": "NEVER-HOST"}
  
