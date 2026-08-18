from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/qa", tags=["QA Dashboard"])

templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
def get_qa_dashboard(request: Request):
    return templates.TemplateResponse(
        "qa_dashboard.html",
        {"request": request}
    )
