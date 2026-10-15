from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="NEVER-HOST")

PAGE = r"""
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#101014">
<title>NEVER-HOST♥️</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#101014;color:#f5f3fa;
font:15px Arial,sans-serif}
header{padding:22px 18px;border-bottom:1px solid #292631;
display:flex;justify-content:space-between;align-items:center}
.logo{font-size:22px;font-weight:800;color:#d5a5ff}
.pill{font-size:12px;border:1px solid #443451;
padding:7px 10px;border-radius:20px;color:#d5a5ff}
main{max-width:760px;margin:30px auto;padding:0 16px}
h1{font-size:32px;margin:0 0 10px}
.sub{color:#aaa5b5;line-height:1.6}
.card{background:#19171f;border:1px solid #302b39;
border-radius:16px;padding:20px;margin:20px 0}
h2{font-size:18px;margin:0 0 16px}
label{display:block;margin:14px 0 8px;color:#c7c1d0}
input,select{width:100%;padding:13px;background:#100f14;
color:white;border:1px solid #484151;border-radius:9px}
button{padding:12px 15px;border:0;border-radius:9px;
background:#a855f7;color:white;font-weight:bold;font-size:14px}
button:disabled{background:#39323f;color:#c2b9ca}
.primary{width:100%;margin-top:16px}
.statrow{display:flex;gap:10px;margin-top:20px}
.stat{flex:1;background:#201c28;border-radius:12px;padding:15px}
.num{font-size:23px;font-weight:bold}
.muted{font-size:12px;color:#aaa5b5;margin-top:6px}
.notice{padding:13px;background:#211a2a;border-radius:10px;
color:#d9c6ee;line-height:1.5;font-size:13px}
.bot{padding:15px 0;border-bottom:1px solid #302b39}
.bot:last-child{border-bottom:0}
.botname{font-weight:bold;margin-bottom:8px}
footer{text-align:center;color:#777181;font-size:12px;padding:24px}
a{color:#d5a5ff}
@media(max-width:420px){h1{font-size:27px}.card{padding:16px}
.stat{padding:11px}.num{font-size:20px}}
</style>
</head>
<body>
<header>
  <div class="logo">NEVER-HOST♥️</div>
  <div class="pill">BETA · TEST</div>
</header>
<main>
  <h1>Твой бот. Твой запуск.</h1>
  <div class="sub">Панель управления Telegram-ботами.<br>
  Всё необходимое — в одном месте.</div>

  <div class="statrow">
    <div class="stat"><div class="num">0</div>
    <div class="muted">Мои боты</div></div>
    <div class="stat"><div class="num">—</div>
    <div class="muted">Запущено</div></div>
    <div class="stat"><div class="num">OK</div>
    <div class="muted">API</div></div>
  </div>

  <section class="card">
    <h2>＋ Добавить бота</h2>
    <div class="notice">
      Загрузка пока не подключена к хранилищу.
      Не вводи токен Telegram и не загружай секретные файлы.
    </div>
    <label for="botname">Название бота</label>
    <input id="botname" placeholder="Например, My Telegram Bot">
    <label for="botfile">Файл бота (.py или .zip)</label>
    <input id="botfile" type="file" accept=".py,.zip">
    <button class="primary" disabled>Загрузка скоро появится</button>
  </section>

  <section class="card">
    <h2>Мои боты</h2>
    <div class="bot">
      <div class="botname">Пока ботов нет</div>
      <div class="muted">Добавление появится после настройки
      безопасного хранения и запуска.</div>
    </div>
  </section>

  <section class="card">
    <h2>Состояние сервера</h2>
    <p class="sub" id="health">Проверяем API…</p>
    <button onclick="checkHealth()">Проверить снова</button>
  </section>
</main>
<footer>NEVER-HOST♥️ · Независимый проект</footer>
<script>
async function checkHealth(){
  const el=document.getElementById('health');
  el.textContent='Проверяем API…';
  try{
    const r=await fetch('/health');
    const d=await r.json();
    el.textContent=r.ok && d.status==='ok'
      ? '● Сервер работает'
      : 'Сервер ответил с ошибкой';
  }catch(e){
    el.textContent='Сервер временно недоступен';
  }
}
checkHealth();
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE

@app.get("/health")
def health():
    return {"status": "ok", "service": "NEVER-HOST"}
    
