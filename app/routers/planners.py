from fastapi import APIRouter

from ..models import (
    BudgetAllocation,
    HomePlannerRequest,
    JewelryPlannerRequest,
    PartyPlannerRequest,
    RecommendationDetailsRequest,
    RecommendationItem,
    RecommendationResponse,
)


router = APIRouter(prefix="/api/planners", tags=["Budget planners"])


def _recommendation(
    planner_type: str,
    budget: float,
    summary: str,
    allocations: list[tuple[str, float]],
    items: list[tuple[str, str, str, float]],
) -> RecommendationResponse:
    item_share = sum(item[3] for item in items)
    return RecommendationResponse(
        planner_type=planner_type,
        budget=budget,
        summary=summary,
        recommendations=[
            RecommendationItem(
                name=name,
                category=category,
                description=description,
                estimated_price=round(budget * share, 2),
                reason="A practical option within the requested budget.",
            )
            for name, category, description, share in items
        ],
        budget_allocation=[
            BudgetAllocation(
                category=category,
                amount=round(budget * share, 2),
                percentage=round(share * 100, 2),
            )
            for category, share in allocations
        ],
        total_estimated_cost=round(budget * item_share, 2),
        remaining_budget=round(budget * (1 - item_share), 2),
        ai_generated=False,
        message="Generated using local fallback recommendations.",
    )


@router.post("/home", response_model=RecommendationResponse)
def plan_home(payload: HomePlannerRequest) -> RecommendationResponse:
    style = payload.style or "Modern"
    room = payload.room_type
    return _recommendation(
        "home",
        payload.budget,
        f"A {style.lower()} {room.lower()} plan within your budget.",
        [("Furniture", 0.42), ("Lighting", 0.23), ("Decor", 0.18), ("Reserve", 0.17)],
        [
            (f"{style} furniture set", "Furniture", f"Essential pieces for a {room.lower()}.", 0.42),
            ("Layered lighting", "Lighting", "Combine ambient and task lighting.", 0.23),
            ("Finishing decor", "Decor", "Add a few coordinated finishing touches.", 0.18),
        ],
    )


@router.post("/party", response_model=RecommendationResponse)
def plan_party(payload: PartyPlannerRequest) -> RecommendationResponse:
    event = payload.event_type
    return _recommendation(
        "party",
        payload.budget,
        f"A practical plan for your {event.lower()} with {payload.guests} guests.",
        [("Venue", 0.35), ("Food", 0.30), ("Decor", 0.20), ("Reserve", 0.15)],
        [
            ("Venue allowance", "Venue", "A venue allocation sized to your guest count.", 0.35),
            ("Food and refreshments", "Food", "Plan portions around the guest count.", 0.30),
            ("Simple event decor", "Decor", "A restrained decoration budget.", 0.20),
        ],
    )


@router.post("/jewelry", response_model=RecommendationResponse)
def plan_jewelry(payload: JewelryPlannerRequest) -> RecommendationResponse:
    style = payload.style or "Elegant"
    occasion = payload.occasion
    return _recommendation(
        "jewelry",
        payload.budget,
        f"A {style.lower()} jewelry plan for {occasion.lower()}.",
        [("Main piece", 0.65), ("Complementary pieces", 0.20), ("Reserve", 0.15)],
        [
            (f"{style} statement piece", "Main piece", f"A focal piece for {occasion.lower()}.", 0.65),
            ("Coordinated accents", "Complementary pieces", "Smaller pieces that complement the main item.", 0.20),
        ],
    )


@router.post("/recommendations-details", response_model=RecommendationResponse)
def recommendation_details(
    payload: RecommendationDetailsRequest,
) -> RecommendationResponse:
    category = payload.category or "Recommended"
    return _recommendation(
        payload.planner_type,
        payload.budget,
        "A budget-conscious recommendation based on your preferences.",
        [(category, 0.85), ("Reserve", 0.15)],
        [
            (
                category,
                category,
                payload.preferences or "A flexible option based on your budget.",
                0.85,
            )
        ],
    )