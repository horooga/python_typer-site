from fastapi import FastAPI, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import yaml
import time
import random

with open("questions.yaml", "r") as f:
    try:
        answers = yaml.safe_load(f)
        questions = [i for i in answers]
        questions_amount = len(questions)
    except Exception as e:
        print(e)
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
            "question": questions[random.randrange(questions_amount)],
            "res": "Question skipped" if not answer else "Awesome!" if answer == answers[question] else "Oh no!",
            "feedback": f"With time elapsed: {str(round(time.time() - float(start_time), 3))}" if answer == answers[question] else f"Answer was: {answers[question]}",
            "start_time": str(round(time.time()))
        })
    else:
        return templates.TemplateResponse("first_type.html", {
            "request": request,
            "question": questions[random.randrange(questions_amount)],
            "start_time": str(round(time.time()))
        })
    
