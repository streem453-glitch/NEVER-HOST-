from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
from uuid import uuid4
import os

app = FastAPI(title="NEVER-HOST")

# Папка для загрузки файлов
UPLOAD_DIR = Path("/tmp/never-host-uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 5 МБ максимальный размер файла
MAX_SIZE = 5 * 1024 * 1024
bots = []

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
body{margin:0;background:#101014;color:#f5f3fa;font:15px Arial,sans-serif}
header{padding:22px 18px;border-bottom:1px solid #292631;display:flex;justify-content:space-between;align-items:center}
.logo{font-size:22px;font-weight:800;color:#d5a5ff}
.pill{font-size:12px;border:1px solid #443451;padding:7px 10px;border-radius:20px;color:#d5a5ff}
main{max-width:760px;margin:30px auto;padding:0 16px}
h1{font-size:32px;margin:0 0 10px}
.sub{color:#aaa5b5;line-height:1.6}
.card{background:#19171f;border:1px solid #302b39;border-radius:16px;padding:20px;margin:20px 0}
h2{font-size:18px;margin:0 0 16px}
label{display:block;margin:14px 0 8px;color:#c7c1d0}
input{width:100%;padding:13px;background:#100f14;color:white;border:1px solid #484151;border-radius:9px}
button{padding:12px 15px;border:0;border-radius:9px;background:#a855f7;color:white;font-weight:bold;font-size:14px;cursor:pointer}
button:disabled{opacity:.5}
.primary{width:100%;margin-top:16px}
.statrow{display:flex;gap:10px;margin-top:20px}
.stat{flex:1;background:#201c28;border-radius:12px;padding:15px}
.num{font-size:23px;font-weight:bold}
.muted{font-size:12px;color:#aaa5b5;margin-top:6px}
.notice{padding:13px;background:#211a2a;border-radius:10px;color:#d9c6ee;line-height:1.5;font-size:13px}

/* Стилизация строки бота и кнопки */
.bot{padding:15px 0;border-bottom:1px solid #302b39;overflow-wrap:anywhere;display:flex;justify-content:space-between;align-items:center;gap:15px}
.bot:last-child{border-bottom:0}
.botname{font-weight:bold;margin-bottom:8px}
.bot-info{flex:1}
.btn-run{background:#22c55e;padding:8px 14px;font-size:13px}
.btn-run.running{background:#ef4444}

footer{text-align:center;color:#777181;font-size:12px;padding:24px}
@media(max-width:420px){h1{font-size:27px}.card{padding:16px}.stat{padding:11px}.num{font-size:20px}.bot{flex-direction:column;align-items:flex-start}.btn-run{width:100%}}
</style>
</head>
<body>
<header><div class="logo">NEVER-HOST♥️</div><div class="pill">BETA · TEST</div></header>
<main>
<h1>Твой бот. Твой запуск.</h1>
<div class="sub">Панель управления Telegram-ботами.<br>Всё необходимое — в одном месте.</div>
<div class="statrow">
<div class="stat"><div class="num" id="count">0</div><div class="muted">Загружено файлов</div></div>
<div class="stat"><div class="num">BETA</div><div class="muted">Режим сервиса</div></div>
<div class="stat"><div class="num" id="api">OK</div><div class="muted">API</div></div>
</div>
<section class="card">
<h2>＋ Добавить бота</h2>
<div class="notice">Принимаются файлы .py и .zip до 5 МБ. Файлы пока только хранятся временно — код не запускается. Не загружай секретные данные.</div>
<form id="uploadForm">
<label for="botname">Название бота</label>
<input id="botname" name="name" maxlength="60" required placeholder="Например, My Telegram Bot">
<label for="botfile">Файл бота (.py или .zip)</label>
<input id="botfile" name="file" type="file" accept=".py,.zip" required>
<button class="primary" id="submitBtn" type="submit">Загрузить файл</button>
</form>
<p class="sub" id="message" role="status"></p>
</section>
<section class="card">
<h2>Мои боты</h2>
<div id="bots"><div class="muted">Загружаем список…</div></div>
</section>
<section class="card">
<h2>Состояние сервера</h2>
<p class="sub" id="health">Проверяем API…</p>
<button type="button" onclick="checkHealth()">Проверить снова</button>
</section>
</main>
<footer>NEVER-HOST♥️ · Независимый проект</footer>
<script>
async function checkHealth(){
 const el=document.getElementById('health');
 try{
  const r=await fetch('/health');
  const d=await r.json();
  el.textContent=r.ok&&d.status==='ok'?'● Сервер работает':'Сервер ответил с ошибкой';
 }catch(e){el.textContent='Сервер временно недоступен';}
}

async function toggleBot(botId, currentStatus, btn) {
  btn.disabled = true;

  try {
    const nextStatus =
      currentStatus === 'running' ? 'uploaded' : 'running';

    const r = await fetch(`/api/bots/${botId}/status`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({status: nextStatus})
    });

    const data = await r.json();

    if (!r.ok) {
      throw new Error(data.detail || 'Ошибка сервера');
    }

    await loadBots();
  } catch (e) {
    alert('Ошибка: ' + e.message);
  } finally {
    btn.disabled = false;
  }
}

async function loadBots(){
 const box=document.getElementById('bots');
 try{
  const r=await fetch('/api/bots');
  if(!r.ok)throw Error();
  const d=await r.json();
  document.getElementById('count').textContent=d.bots.length;
  box.innerHTML='';
  if(!d.bots.length){box.innerHTML='<div class="muted">Пока файлов нет. Загрузи первый!</div>';return;}
  d.bots.forEach(b=>{
   const item=document.createElement('div');item.className='bot';
   
   const infoContainer=document.createElement('div');infoContainer.className='bot-info';
   const name=document.createElement('div');name.className='botname';name.textContent=b.name;
   
   const isRun = b.status === 'running';
   const statusText = isRun ? 'Запущен, работает' : 'Загружен, не запущен';
   
   const info=document.createElement('div');info.className='muted';
   info.textContent=b.filename+' · '+b.size+' байт · ' + statusText;
   infoContainer.append(name,info);
   
   const runBtn=document.createElement('button');
   runBtn.type='button';
   runBtn.className = isRun ? 'btn-run running' : 'btn-run';
   runBtn.textContent = isRun ? 'Остановить' : 'Запустить';
   runBtn.onclick = () => toggleBot(b.id, b.status, runBtn);
   
   item.append(infoContainer, runBtn);
   box.append(item);
  });
 }catch(e){box.textContent='Не удалось загрузить список.';}
}

document.getElementById('uploadForm').addEventListener('submit',async e=>{
 e.preventDefault();
 const form=e.currentTarget,btn=document.getElementById('submitBtn'),msg=document.getElementById('message');
 
 const file=document.getElementById('botfile').files[0];
 if(!file){msg.textContent='Выбери файл.';return;}
 if(file.size>5*1024*1024){msg.textContent='Файл больше 5 МБ.';return;}
 
 btn.disabled=true;msg.textContent='Загружаем…';
 try{
  const r=await fetch('/api/bots',{method:'POST',body:new FormData(form)});
  const d=await r.json();
  if(!r.ok)throw Error(d.detail||'Ошибка загрузки');
  msg.textContent='Файл загружен! Код не запускался.';
  form.reset();await loadBots();
 }catch(err){msg.textContent='Ошибка: '+err.message;}
 finally{btn.disabled=false;}
});
checkHealth();loadBots();
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

@app.get("/api/bots")
def list_bots():
    return {"bots": bots}

from pydantic import BaseModel
class StatusUpdate(BaseModel):
    status: str

# Обновленный эндпоинт, возвращающий ошибку 501
@app.post("/api/bots/{bot_id}/status")
def update_bot_status(bot_id: str, payload: StatusUpdate):
    raise HTTPException(
        status_code=501,
        detail=(
            "Запуск процессов пока не подключён. "
            "Файл загружен, но бот не запущен."
        )
    )

@app.post("/api/bots")
async def upload_bot(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    name = name.strip()
    if not name or len(name) > 60:
        raise HTTPException(400, "Название должно содержать от 1 до 60 символов")

    filename = Path(file.filename or "").name
    ext = Path(filename).suffix.lower()
    if ext not in {".py", ".zip"}:
        raise HTTPException(400, "Разрешены только файлы .py и .zip")

    bot_id = uuid4().hex
    target = UPLOAD_DIR / f"{bot_id}{ext}"
    
    try:
        content = await file.read()
        size = len(content)
        
        if size > MAX_SIZE:
            raise HTTPException(413, "Максимальный размер файла — 5 МБ")
            
        with target.open("wb") as out:
            out.write(content)
            
    except HTTPException:
        target.unlink(missing_ok=True)
        raise
    except Exception:
        target.unlink(missing_ok=True)
        raise HTTPException(500, "Внутренняя ошибка сервера при записи файла")
    finally:
        await file.close()

    bot = {
        "id": bot_id,
        "name": name,
        "filename": filename,
        "size": size,
        "status": "uploaded"
    }
    bots.append(bot)
    return {"ok": True, "bot": bot}
 
