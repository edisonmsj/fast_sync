import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fast_zero.routers import auth, todo, users

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)


# Caminho absoluto para o diretório 'static'
static_directory = os.path.join(os.getcwd(), 'static')

# Monta a pasta 'static' como a raiz para arquivos estáticos
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(),
 "fast_zero", "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    landing_page_path = os.path.join(
        os.getcwd(), "fast_zero", "static", "templates", "landing_page.html")
    with open(landing_page_path, "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())