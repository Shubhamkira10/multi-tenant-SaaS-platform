from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    tags=["Dashboard"]
)


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="dashboard.html",
    context={
        "app_name": "Mail Automation Platform",
        "version": "1.0.0",
        "environment": "Development",
    },
)