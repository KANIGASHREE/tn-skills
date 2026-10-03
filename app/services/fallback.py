from .catalog import search_catalog


def pick(
    items,
    budget,
    limit
):

    selected = []

    total = 0

    for item in items:

        if total + item["price"] <= budget:

            result = dict(item)

            result.update(
                {
                    "quantity": 1,
                    "total": float(
                        item["price"]
                    ),
                    "reason":
                        "Selected to fit the requested budget and category."
                }
            )

            selected.append(result)

            total += item["price"]

        if len(selected) >= limit:
            break

    return selected, total


def home_recommendations(request):

    items = search_catalog(
        {
            "lighting",
            "fan",
            "furniture",
            "decor"
        },
        f"{request.room_type} "
        f"{request.style} "
        f"{request.requirements}"
    )

    recommendations, total = pick(
        items,
        request.budget * 0.95,
        7
    )

    return {

        "planner": "home",

        "budget": request.budget,

        "estimated_total":
            round(total, 2),

        "remaining":
            round(
                request.budget - total,
                2
            ),

        "summary":
            f"A {request.style} "
            f"{request.room_type} setup "
            "focused on practical essentials "
            "and budget control.",

        "allocations": {

            "furniture":
                round(
                    request.budget * 0.45,
                    2
                ),

            "lighting":
                round(
                    request.budget * 0.20,
                    2
                ),

            "decor":
                round(
                    request.budget * 0.20,
                    2
                ),

            "flexible":
                round(
                    request.budget * 0.15,
                    2
                )
        },

        "recommendations":
            recommendations,

        "source":
            "fallback",

        "ai_notes": [
            "Local catalog mode is active. "
            "Replace it with official marketplace APIs "
            "for live data."
        ]
    }


def party_recommendations(request):

    allocations = {

        "catering":
            round(
                request.budget * 0.50,
                2
            ),

        "decoration":
            round(
                request.budget * 0.20,
                2
            ),

        "venue":
            round(
                request.budget * 0.20,
                2
            ),

        "entertainment":
            round(
                request.budget * 0.10,
                2
            )
    }

    items = search_catalog(
        {
            "catering",
            "decoration",
            "venue"
        },
        f"{request.event_type} "
        f"party "
        f"{request.preferences}"
    )

    recommendations = []

    total = 0

    for item in items:

        if item["category"] == "catering":

            cost = (
                item["price"]
                * request.guests
            )

            quantity = request.guests

        else:

            cost = item["price"]

            quantity = 1

        if (
            total + cost
            <= request.budget * 0.95
        ):

            result = dict(item)

            result.update(
                {
                    "quantity": quantity,
                    "total": float(cost),
                    "reason":
                        "Scaled for guest count "
                        "and kept within the event budget."
                }
            )

            recommendations.append(
                result
            )

            total += cost

        if len(recommendations) >= 6:
            break

    return {

        "planner": "party",

        "budget": request.budget,

        "estimated_total":
            round(total, 2),

        "remaining":
            round(
                request.budget - total,
                2
            ),

        "summary":
            f"A {request.event_type} plan "
            f"for {request.guests} guests "
            f"in {request.city}, prioritizing "
            "catering, venue and decoration.",

        "allocations":
            allocations,

        "recommendations":
            recommendations,

        "source":
            "fallback",

        "ai_notes": [
            "Vendor data is simulated locally. "
            "Connect official vendor APIs "
            "for live availability."
        ]
    }


def jewelry_recommendations(
    request,
    image=False
):

    items = search_catalog(
        {
            "necklace",
            "earrings",
            "bracelet"
        },
        f"{request.occasion} "
        f"{request.style} "
        f"{request.preferences}"
    )

    recommendations, total = pick(
        items,
        request.budget * 0.95,
        6
    )

    if image:

        note = (
            "Outfit image received. "
            "Gemini can analyze it when configured."
        )

    else:

        note = (
            "No outfit image supplied."
        )

    return {

        "planner":
            "jewelry",

        "budget":
            request.budget,

        "estimated_total":
            round(total, 2),

        "remaining":
            round(
                request.budget - total,
                2
            ),

        "summary":
            f"Jewelry options for a "
            f"{request.occasion} occasion "
            f"with a {request.style} "
            "style preference.",

        "allocations": {

            "necklace":
                round(
                    request.budget * 0.40,
                    2
                ),

            "earrings":
                round(
                    request.budget * 0.30,
                    2
                ),

            "bracelet":
                round(
                    request.budget * 0.20,
                    2
                ),

            "flexible":
                round(
                    request.budget * 0.10,
                    2
                )
        },

        "recommendations":
            recommendations,

        "source":
            "fallback",

        "ai_notes": [
            note
        ]
    }