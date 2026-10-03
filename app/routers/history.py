from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import current_user

from ..models.recommendation import Recommendation


router = APIRouter(
    tags=["History"]
)


@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    user=Depends(current_user)
):

    rows = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == user.id
        )
        .order_by(
            Recommendation.created_at.desc()
        )
        .limit(50)
        .all()
    )

    return [
        {
            "id": row.id,
            "planner_type": row.planner_type,
            "budget": row.budget,
            "source": row.source,
            "created_at": row.created_at.isoformat(),
            "result": row.result_data
        }
        for row in rows
    ]


@router.get("/history/{recommendation_id}")
def get_history_detail(
    recommendation_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):

    row = db.get(
        Recommendation,
        recommendation_id
    )

    if (
        not row
        or row.user_id != user.id
    ):

        raise HTTPException(
            status_code=404,
            detail="History item not found"
        )

    return {
        "id": row.id,
        "planner_type": row.planner_type,
        "budget": row.budget,
        "request": row.request_data,
        "result": row.result_data
    }