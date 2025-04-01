from fastapi import FastAPI, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import yaml
import time

with open("questions.yaml", "r") as f:
    answers = yaml.safe_load(f)
    questions = [i for i in answers]
app = FastAPI()
templates = Jinja2Templates(directory="static")
app.mount("/static", StaticFiles(directory="static"))

@app.get("/")
async def start(response_class = HTMLResponse):
    return FileResponse("static/start.html")

@app.post("/type")
async def type(request: Request, question: str = Form(default = None), answer: str = Form(default = None), start_time: str = Form(default = None), response_class = HTMLResponse):
    if start_time:
        return templates.TemplateResponse("type.html", {
            "request": request,
            "question": questions[1],
            "res": "Awesome!" if answer == answers[question] else "Oh no!",
            "time_elapsed": str(round(time.time() - float(start_time), 3)),
            "start_time": str(round(time.time()))
        })
    else:
        return templates.TemplateResponse("first_type.html", {
            "request": request,
            "question": questions[1],
            "start_time": str(round(time.time()))
        })
    
