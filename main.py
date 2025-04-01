from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="static")
app.mount("/static", StaticFiles(directory="static"))
questions = ["one plus two = ?", "color of a cow's milk is - ?"]

@app.get("/")
async def start(request: Request, response_class = HTMLResponse):
    return templates.TemplateResponse("start.html", {"request": request})

@app.post("/type")
async def type(request: Request, response_class = HTMLResponse):
    return templates.TemplateResponse("type.html", {"request": request, "question": questions[0]})
