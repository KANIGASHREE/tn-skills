import base64
import json

from ..config import settings

from .fallback import (
    home_recommendations,
    party_recommendations,
    jewelry_recommendations
)

from .catalog import marketplace_url


class GeminiService:

    def __init__(self):

        self.enabled = bool(
            settings.gemini_api_key
        )

        self.client = None

        if self.enabled:

            try:

                from google import genai

                self.client = genai.Client(
                    api_key=settings.gemini_api_key
                )

            except Exception:

                self.enabled = False


    def generate(
        self,
        planner,
        data,
        image_bytes=None,
        mime_type=None
    ):

        if not self.enabled:
            return None

        prompt = f"""
You are PocketSmart AI.

Create a budget-aware {planner} plan.

User data:

{json.dumps(data)}

Return ONLY valid JSON.

Required JSON keys:

summary
allocations
recommendations
ai_notes

Each recommendation must contain:

name
category
platform
price
quantity
total
reason

Use Indian rupees.

Do not exceed the user's budget.

Allowed platform names include:

Amazon
Flipkart
IKEA
Swiggy
Zomato
OYO

Do not claim live inventory.

Provide practical recommendations.
"""

        try:

            contents = [
                prompt
            ]

            if image_bytes and mime_type:

                contents.append(
                    {
                        "inline_data": {
                            "mime_type":
                                mime_type,

                            "data":
                                base64.b64encode(
                                    image_bytes
                                ).decode()
                        }
                    }
                )

                contents[0] += """

Analyze the outfit image only
for broad colors and fashion style.

Do not infer sensitive personal attributes.
"""

            response = (
                self.client.models.generate_content(
                    model=settings.gemini_model,
                    contents=contents
                )
            )

            text = (
                response.text or ""
            ).strip()

            if text.startswith("```"):

                text = (
                    text
                    .split("\n", 1)[1]
                    .rsplit("```", 1)[0]
                )

            return json.loads(text)

        except Exception:

            return None


    def recommend(
        self,
        planner,
        request,
        image_bytes=None,
        mime_type=None
    ):

        data = request.model_dump()

        ai_result = self.generate(
            planner,
            data,
            image_bytes,
            mime_type
        )

        if ai_result:

            budget = float(
                data["budget"]
            )

            recommendations = []

            total = 0

            for item in ai_result.get(
                "recommendations",
                []
            ):

                try:

                    price = float(
                        item["price"]
                    )

                    quantity = max(
                        1,
                        int(
                            item.get(
                                "quantity",
                                1
                            )
                        )
                    )

                    cost = (
                        price * quantity
                    )

                    if price <= 0:
                        continue

                    if (
                        total + cost
                        > budget
                    ):
                        continue

                    platform = str(
                        item.get(
                            "platform",
                            "Amazon"
                        )
                    )

                    name = str(
                        item.get(
                            "name",
                            "Recommendation"
                        )
                    )

                    recommendations.append(
                        {
                            "name": name,

                            "category":
                                str(
                                    item.get(
                                        "category",
                                        "general"
                                    )
                                ),

                            "platform":
                                platform,

                            "price":
                                price,

                            "quantity":
                                quantity,

                            "total":
                                cost,

                            "reason":
                                str(
                                    item.get(
                                        "reason",
                                        "AI budget-aware recommendation."
                                    )
                                ),

                            "url":
                                marketplace_url(
                                    platform,
                                    name
                                )
                        }
                    )

                    total += cost

                except Exception:

                    continue

            if recommendations:

                allocations = {}

                for key, value in (
                    ai_result
                    .get(
                        "allocations",
                        {}
                    )
                    .items()
                ):

                    try:

                        allocations[
                            str(key)
                        ] = float(value)

                    except Exception:

                        pass

                return {

                    "planner":
                        planner,

                    "budget":
                        budget,

                    "estimated_total":
                        round(total, 2),

                    "remaining":
                        round(
                            budget - total,
                            2
                        ),

                    "summary":
                        str(
                            ai_result.get(
                                "summary",
                                "AI-generated plan"
                            )
                        ),

                    "allocations":
                        allocations,

                    "recommendations":
                        recommendations,

                    "source":
                        "gemini",

                    "ai_notes":
                        [
                            str(x)
                            for x in
                            ai_result.get(
                                "ai_notes",
                                []
                            )
                        ]
                }

        if planner == "home":

            return home_recommendations(
                request
            )

        if planner == "party":

            return party_recommendations(
                request
            )

        return jewelry_recommendations(
            request,
            bool(image_bytes)
        )


gemini_service = GeminiService()