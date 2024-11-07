from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import googlesheets

app = FastAPI()


# Подключаем папку static для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Роут для отображения index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), media_type="text/html; charset=utf-8")
    
@app.post("/register")
async def hello(data = Body()):
    if 'number_action' in data and 'fio' in data and 'phone_number' in data and 'timezone' in data:
        temp_ = googlesheets.register_action(data['number_action'],
                                     data['fio'],
                                     data['phone_number'],
                                     data['timezone'])
        return {True}
    else:
        return {False}