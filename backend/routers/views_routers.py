from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()


templates_dir = "./frontend/templates"
templates = Jinja2Templates(directory=templates_dir)


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("home_page.html", {"request": request})


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/cadastro")
def cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})
