from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class RegisterRequest(BaseModel):

    email: str = Field(
        min_length=5,
        max_length=255
    )

    full_name: str = Field(
        min_length=2,
        max_length=120
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: str

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    room_type: str = Field(
        min_length=2,
        max_length=50
    )

    style: str = Field(
        default="modern",
        min_length=2,
        max_length=50
    )

    requirements: str = Field(
        default="",
        max_length=1000
    )

    quantities: dict[str, int] = {}

    @field_validator("quantities")
    @classmethod
    def validate_quantities(cls, value):

        if len(value) > 30:
            raise ValueError(
                "Too many quantity entries"
            )

        for quantity in value.values():

            quantity = int(quantity)

            if quantity < 1 or quantity > 100:
                raise ValueError(
                    "Quantity must be between 1 and 100"
                )

        return {
            str(key): int(quantity)
            for key, quantity in value.items()
        }


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=10000
    )

    event_type: str = Field(
        min_length=2,
        max_length=50
    )

    venue: str = Field(
        default="indoor",
        max_length=100
    )

    city: str = Field(
        default="Chennai",
        max_length=100
    )

    preferences: str = Field(
        default="",
        max_length=1000
    )


class RecommendationResponse(BaseModel):

    planner: str

    budget: float

    estimated_total: float

    remaining: float

    summary: str

    allocations: dict[str, float]

    recommendations: list[dict]

    source: str

    ai_notes: list[str] = []