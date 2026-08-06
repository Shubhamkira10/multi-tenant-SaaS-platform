from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.platform.dashboard.service import DashboardService
from app.shared.schemas import ApiResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.get(
    "",
    response_model=ApiResponse[dict],
)
def dashboard(
    db: Session = Depends(get_db),
):

    return ApiResponse(
        success=True,
        message="Success",
        data=DashboardService(db).get_stats(),
    )