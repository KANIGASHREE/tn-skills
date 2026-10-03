from urllib.parse import quote


CATALOG = [

    {
        "name": "Minimal LED Ceiling Light",
        "category": "lighting",
        "platform": "IKEA",
        "price": 1499,
        "keywords": "living bedroom modern"
    },

    {
        "name": "3-Blade Ceiling Fan",
        "category": "fan",
        "platform": "Amazon",
        "price": 2499,
        "keywords": "living bedroom kitchen"
    },

    {
        "name": "Compact Study Table",
        "category": "furniture",
        "platform": "Amazon",
        "price": 3999,
        "keywords": "bedroom study modern"
    },

    {
        "name": "6-Seater Dining Table",
        "category": "furniture",
        "platform": "IKEA",
        "price": 15999,
        "keywords": "dining kitchen"
    },

    {
        "name": "Wall Art Set",
        "category": "decor",
        "platform": "Flipkart",
        "price": 899,
        "keywords": "living bedroom decor"
    },

    {
        "name": "Cushion Set",
        "category": "decor",
        "platform": "IKEA",
        "price": 799,
        "keywords": "living decor"
    },

    {
        "name": "Indoor Plant Pot",
        "category": "decor",
        "platform": "Amazon",
        "price": 499,
        "keywords": "living bedroom decor"
    },

    {
        "name": "Party Veg Catering Pack",
        "category": "catering",
        "platform": "Zomato",
        "price": 350,
        "keywords": "birthday wedding corporate"
    },

    {
        "name": "Party Snacks Pack",
        "category": "catering",
        "platform": "Swiggy",
        "price": 220,
        "keywords": "birthday party"
    },

    {
        "name": "Balloon Decoration Kit",
        "category": "decoration",
        "platform": "Amazon",
        "price": 1299,
        "keywords": "birthday wedding party"
    },

    {
        "name": "Elegant Table Decor Set",
        "category": "decoration",
        "platform": "Flipkart",
        "price": 1899,
        "keywords": "wedding corporate party"
    },

    {
        "name": "Budget Event Room",
        "category": "venue",
        "platform": "OYO",
        "price": 4500,
        "keywords": "birthday corporate party"
    },

    {
        "name": "Classic Gold-Plated Necklace",
        "category": "necklace",
        "platform": "Amazon",
        "price": 1799,
        "keywords": "wedding festive traditional"
    },

    {
        "name": "Pearl Drop Earrings",
        "category": "earrings",
        "platform": "Flipkart",
        "price": 899,
        "keywords": "wedding formal elegant"
    },

    {
        "name": "Minimal Hoop Earrings",
        "category": "earrings",
        "platform": "Amazon",
        "price": 599,
        "keywords": "casual modern"
    },

    {
        "name": "Crystal Bracelet",
        "category": "bracelet",
        "platform": "Flipkart",
        "price": 749,
        "keywords": "party modern elegant"
    },

    {
        "name": "Kundan Stud Set",
        "category": "earrings",
        "platform": "Amazon",
        "price": 1299,
        "keywords": "wedding festive traditional"
    }
]


def marketplace_url(
    platform: str,
    name: str
):

    query = quote(name)

    urls = {

        "Amazon":
            f"https://www.amazon.in/s?k={query}",

        "Flipkart":
            f"https://www.flipkart.com/search?q={query}",

        "IKEA":
            f"https://www.ikea.com/in/en/search/?q={query}",

        "Swiggy":
            f"https://www.swiggy.com/search?query={query}",

        "Zomato":
            f"https://www.zomato.com/search?q={query}",

        "OYO":
            f"https://www.oyorooms.com/search?location=Chennai&query={query}"
    }

    return urls.get(
        platform,
        f"https://www.google.com/search?q={query}"
    )


def search_catalog(
    categories,
    keywords=""
):

    words = set(
        keywords.lower().split()
    )

    rows = []

    for item in CATALOG:

        if item["category"] not in categories:
            continue

        item_words = set(
            item["keywords"].split()
        )

        score = len(
            words.intersection(item_words)
        )

        rows.append(
            (
                score,
                item
            )
        )

    rows.sort(
        key=lambda row: (
            -row[0],
            row[1]["price"]
        )
    )

    return [
        {
            **item,
            "url": marketplace_url(
                item["platform"],
                item["name"]
            )
        }
        for _, item in rows
    ]