from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr


# ============================================================
# USER / AUTHENTICATION MODELS
# ============================================================

class UserCreate(BaseModel):
    """
    Model used when a new user registers.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username"
    )

    email: EmailStr = Field(
        ...,
        description="User email address"
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="User password"
    )


class UserLogin(BaseModel):
    """
    Model used for user login.
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Public user information returned by the API.
    """

    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


# ============================================================
# TOKEN / AUTHENTICATION RESPONSE
# ============================================================

class Token(BaseModel):
    """
    JWT authentication response.
    """

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Data stored/decoded from a JWT token.
    """

    user_id: Optional[int] = None
    email: Optional[str] = None


# ============================================================
# HOME INTERIOR PLANNER
# ============================================================

class HomePlannerRequest(BaseModel):
    """
    Input model for the Home Interior Budget Planner.
    """

    budget: float = Field(
        ...,
        gt=0,
        description="Total available budget"
    )

    room_type: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Type of room"
    )

    style: Optional[str] = Field(
        default="Modern",
        max_length=100,
        description="Preferred interior style"
    )

    quantity_lights: int = Field(
        default=0,
        ge=0,
        description="Number of lights required"
    )

    quantity_fans: int = Field(
        default=0,
        ge=0,
        description="Number of ceiling fans required"
    )

    quantity_tables: int = Field(
        default=0,
        ge=0,
        description="Number of tables required"
    )

    quantity_chairs: int = Field(
        default=0,
        ge=0,
        description="Number of chairs required"
    )

    quantity_decor: int = Field(
        default=0,
        ge=0,
        description="Number of decorative items required"
    )

    preferences: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Additional home interior preferences"
    )


# ============================================================
# PARTY PLANNER
# ============================================================

class PartyPlannerRequest(BaseModel):
    """
    Input model for the Party Budget Planner.
    """

    budget: float = Field(
        ...,
        gt=0,
        description="Total party budget"
    )

    event_type: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Type of event"
    )

    guests: int = Field(
        ...,
        gt=0,
        le=10000,
        description="Number of guests"
    )

    venue: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Preferred venue or location"
    )

    food_preference: Optional[str] = Field(
        default="Mixed",
        max_length=200,
        description="Food preference"
    )

    decoration_style: Optional[str] = Field(
        default="Simple",
        max_length=200,
        description="Preferred decoration style"
    )

    entertainment: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Entertainment requirements"
    )

    preferences: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Additional party preferences"
    )


# ============================================================
# JEWELRY PLANNER
# ============================================================

class JewelryPlannerRequest(BaseModel):
    """
    Input model for the Jewelry Budget Planner.

    The actual outfit image is received separately through
    FastAPI UploadFile because Pydantic models do not directly
    represent uploaded files.
    """

    budget: float = Field(
        ...,
        gt=0,
        description="Jewelry budget"
    )

    occasion: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Occasion for wearing the jewelry"
    )

    style: Optional[str] = Field(
        default="Elegant",
        max_length=100,
        description="Preferred jewelry style"
    )

    jewelry_type: Optional[str] = Field(
        default="Any",
        max_length=100,
        description="Preferred jewelry type"
    )

    metal_preference: Optional[str] = Field(
        default="Any",
        max_length=100,
        description="Preferred metal"
    )

    preferences: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Additional jewelry preferences"
    )


# ============================================================
# RECOMMENDATION ITEM
# ============================================================

class RecommendationItem(BaseModel):
    """
    Represents one AI-generated recommendation.
    """

    name: str = Field(
        ...,
        description="Product or service name"
    )

    category: Optional[str] = Field(
        default=None,
        description="Recommendation category"
    )

    description: Optional[str] = Field(
        default=None,
        description="Short recommendation description"
    )

    estimated_price: Optional[float] = Field(
        default=None,
        ge=0,
        description="Estimated price"
    )

    platform: Optional[str] = Field(
        default=None,
        description="Suggested platform"
    )

    reason: Optional[str] = Field(
        default=None,
        description="Why this recommendation suits the user"
    )

    link: Optional[str] = Field(
        default=None,
        description="Product/platform URL"
    )


# ============================================================
# BUDGET ALLOCATION
# ============================================================

class BudgetAllocation(BaseModel):
    """
    Represents how the available budget is distributed.
    """

    category: str

    amount: float = Field(
        ...,
        ge=0
    )

    percentage: float = Field(
        ...,
        ge=0,
        le=100
    )


# ============================================================
# RECOMMENDATION RESPONSE
# ============================================================

class RecommendationResponse(BaseModel):
    """
    Standard response returned by the recommendation endpoints.
    """

    success: bool = True

    planner_type: Literal[
        "home",
        "party",
        "jewelry"
    ]

    budget: float

    summary: Optional[str] = None

    recommendations: List[RecommendationItem] = Field(
        default_factory=list
    )

    budget_allocation: List[BudgetAllocation] = Field(
        default_factory=list
    )

    total_estimated_cost: Optional[float] = None

    remaining_budget: Optional[float] = None

    ai_generated: bool = False

    message: Optional[str] = None


# ============================================================
# SESSION MODELS
# ============================================================

class SessionInfo(BaseModel):
    """
    Basic information about the current session.
    """

    logged_in: bool
    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None


class SessionData(BaseModel):
    """
    Detailed session information used for personalization.
    """

    user_id: Optional[int] = None

    last_planner: Optional[
        Literal["home", "party", "jewelry"]
    ] = None

    last_budget: Optional[float] = None

    last_query: Optional[str] = None


# ============================================================
# RECOMMENDATION HISTORY
# ============================================================

class RecommendationHistoryItem(BaseModel):
    """
    One saved recommendation history record.
    """

    id: int

    user_id: int

    planner_type: Literal[
        "home",
        "party",
        "jewelry"
    ]

    budget: float

    query: Optional[str] = None

    summary: Optional[str] = None

    created_at: Optional[str] = None

    recommendations: List[
        RecommendationItem
    ] = Field(
        default_factory=list
    )


class RecommendationHistoryResponse(BaseModel):
    """
    Response containing recommendation history.
    """

    success: bool = True

    history: List[
        RecommendationHistoryItem
    ] = Field(
        default_factory=list
    )


# ============================================================
# DETAILED RECOMMENDATION REQUEST
# ============================================================

class RecommendationDetailsRequest(BaseModel):
    """
    Request model for /recommendations-details.
    """

    planner_type: Literal[
        "home",
        "party",
        "jewelry"
    ]

    budget: float = Field(
        ...,
        gt=0
    )

    preferences: Optional[str] = Field(
        default=None,
        max_length=2000
    )

    category: Optional[str] = Field(
        default=None,
        max_length=200
    )


# ============================================================
# GENERIC API RESPONSE
# ============================================================

class APIResponse(BaseModel):
    """
    Generic API response model.
    """

    success: bool

    message: str

    data: Optional[dict] = None
