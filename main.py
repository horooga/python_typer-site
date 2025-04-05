from fastapi import FastAPI, APIRouter, Request, Form, Body
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from auth import *
import yaml
import time
import random

with open("users.yaml", "r") as f:
    try:
        users = yaml.safe_load(f)
    except Exception as e:
        print(e)

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
            "res": "skip" if not answer else "true" if answer == answers[question] else "false",
            "feedback": f"Time elapsed: {str(round(time.time() - float(start_time), 3))} seconds" if answer == answers[question] else f"Answer was: {answers[question]}",
            "start_time": str(round(time.time()))
        })
    else:
        return templates.TemplateResponse("first_type.html", {
            "request": request,
            "question": questions[random.randrange(questions_amount)],
            "start_time": str(round(time.time()))
        })

@app.post("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/auth")
async def auth(request: Request, username: str = Form(), password: str = Form()):
    if username in users:
        if PASSWORD_CONTEXT.verify(password, users[username]):
            return sign_jwt(username)
        elif True:
            return RedirectResponse("/type", status_code = 302)

