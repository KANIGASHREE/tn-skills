from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import current_user

from ..models.recommendation import Recommendation

from ..schemas import HomeRequest
from ..schemas import PartyRequest
from ..schemas import RecommendationResponse

from ..services.gemini_service import gemini_service


router = APIRouter(
    tags=["Planners"]
)


def save_recommendation(
    db,
    user,
    planner,
    request_data,
    result
):

    recommendation = Recommendation(
        user_id=user.id,
        planner_type=planner,
        budget=result["budget"],
        request_data=request_data,
        result_data=result,
        source=result["source"]
    )

    db.add(recommendation)
    db.commit()


@router.post(
    "/generate-home",
    response_model=RecommendationResponse
)
def generate_home(
    payload: HomeRequest,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):

    result = gemini_service.recommend(
        "home",
        payload
    )

    save_recommendation(
        db,
        user,
        "home",
        payload.model_dump(),
        result
    )

    return result


@router.post(
    "/generate-party",
    response_model=RecommendationResponse
)
def generate_party(
    payload: PartyRequest,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):

    result = gemini_service.recommend(
        "party",
        payload
    )

    save_recommendation(
        db,
        user,
        "party",
        payload.model_dump(),
        result
    )

    return result


@router.post(
    "/generate-jewelry",
    response_model=RecommendationResponse
)
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    preferences: str = Form(""),
    outfit_image: UploadFile | None = File(None),

    db: Session = Depends(get_db),

    user=Depends(current_user)
):

    if outfit_image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if outfit_image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail="Only JPG, PNG or WEBP images are allowed"
            )

    data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "preferences": preferences
    }

    class JewelryPayload:

        def model_dump(self):
            return data

    image_bytes = None
    mime_type = None

    if outfit_image:

        image_bytes = await outfit_image.read()

        if len(image_bytes) > 5 * 1024 * 1024:

            raise HTTPException(
                status_code=413,
                detail="Image is larger than 5 MB"
            )

        mime_type = outfit_image.content_type

    result = gemini_service.recommend(
        "jewelry",
        JewelryPayload(),
        image_bytes,
        mime_type
    )

    save_recommendation(
        db,
        user,
        "jewelry",
        data,
        result
    )

    return result


@router.get(
    "/recommendations-details/{recommendation_id}",
    response_model=RecommendationResponse
)
def recommendation_details(
    recommendation_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):

    recommendation = db.get(
        Recommendation,
        recommendation_id
    )

    if (
        not recommendation
        or recommendation.user_id != user.id
    ):

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    return recommendation.result_data