from typing import Optional
import json
from backend_common.database import Database
from database_transformations.product_schema import SCHEMA
from database_transformations.sample_product_data import SAMPLE_PRODUCT
from typing import List, Dict


async def create_product_table() -> None:
    # Create table if it doesn't exist

    columns = "".join([f"{k} {v}," for k, v in SCHEMA.items()]).strip(",")
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS Product (
            {columns}
    );
    """
    await Database.execute(create_table_query)
    columns = "".join([f"{k}, " for k in SCHEMA.keys()]).rstrip(", ")
    await insert_product(columns)


async def insert_product(columns: str) -> None:
    # Create table if it doesn't exist
    entries = SAMPLE_PRODUCT
    placeholders = "".join(
        [f"${i + 1}, " for i in range(len(entries[0].values()))]
    ).rstrip(", ")
    entries = [list(entry.values()) for entry in entries]
    query = f"""
        INSERT INTO Product ({columns})  
            VALUES({placeholders})
        On CONFLICT(id) DO NOTHING;
        """
    await Database.execute_many(query, entries)


async def get_recommended_products(req: Optional[object] = None) -> dict:
    query = f"""
    SELECT * FROM "schema-marketplace".products
    ;"""
    product_info = dict((await Database.fetchrow(query)).items())
    product_info["userrating"] = json.loads(product_info["userrating"])

    # fetch banner images
    query_banner = """SELECT * FROM "schema-app_generic".banners
    ORDER BY RANDOM()
    LIMIT 1;"""
    banner_item = dict((await Database.fetchrow(query_banner)).items())
    image_banner_url = banner_item["url"]

    data = {
        "justForYou": product_info,
        "bestPick": product_info,
        "bannerImageUrl": image_banner_url,
    }
    return data


async def get_preference_product_detail():
    query = """SELECT * FROM "schema-marketplace".products;"""
    rows = await Database.fetch(query)
    products = list(map(dict, rows))
    for product in products:
        product["userrating"] = json.loads(product["userrating"])
    return {"products": products}


async def get_favorite_products(req: Optional[object] = None) -> List[Dict]:

    ## Waiting for Logic
    data = {
        "products": [
            {"id": 101, "name": "Espresso", "searchType": "scan"},
            {"id": 102, "name": "Cappuccino", "searchType": "search"},
            {"id": 103, "name": "Latte", "searchType": "scan"},
            {"id": 104, "name": "Americano", "searchType": "search"},
        ]
    }
    return data


async def get_user_reviews(req: Optional[object] = None) -> List[Dict]:

    ## Waiting for Logic
    data = {
        "reviews": [
            {
                "id": 201,
                "name": "John Doe",
                "userProfileImageUrl": "https://example.com/images/john_doe.jpg",
                "description": "Great product, highly recommend!",
                "averageRating": 4.5,
                "totalRatings": 120,
                "time": "2 months ago",
            },
            {
                "id": 202,
                "name": "Jane Smith",
                "userProfileImageUrl": "https://example.com/images/jane_smith.jpg",
                "description": "Good quality, but a bit overpriced.",
                "averageRating": 3.8,
                "totalRatings": 85,
                "time": "2 months ago",
            },
            {
                "id": 203,
                "name": "Alex Johnson",
                "userProfileImageUrl": "https://example.com/images/alex_johnson.jpg",
                "description": "Exceeded my expectations. Will buy again!",
                "averageRating": 4.9,
                "totalRatings": 200,
                "time": "2 months ago",
            },
            {
                "id": 204,
                "name": "Emily Brown",
                "userProfileImageUrl": "https://example.com/images/emily_brown.jpg",
                "description": "Not as described, disappointed.",
                "averageRating": 2.1,
                "totalRatings": 45,
                "time": "2 months ago",
            },
        ]
    }

    return data


async def get_coffee_bean_types(req: Optional[object] = None) -> dict:
    data = {
        "coffeeBeanTypes": [
            {"id": 1, "name": "Arabica", "colorCode": "#C19A6B"},
            {"id": 2, "name": "Robusta", "colorCode": "#8B5A2B"},
            {"id": 3, "name": "Liberica", "colorCode": "#A0522D"},
            {"id": 4, "name": "Excelsa", "colorCode": "#D2B48C"},
        ]
    }
    return data


async def get_coffee_types(req: Optional[object] = None) -> dict:
    data = {
        "products": [
            {
                "id": 1,
                "type": "Espresso",
                "imageUrl": "https://example.com/images/espresso.jpg",
            },
            {
                "id": 2,
                "type": "Latte",
                "imageUrl": "https://example.com/images/latte.jpg",
            },
            {
                "id": 3,
                "type": "Cappuccino",
                "imageUrl": "https://example.com/images/cappuccino.jpg",
            },
            {
                "id": 4,
                "type": "Americano",
                "imageUrl": "https://example.com/images/americano.jpg",
            },
            {
                "id": 5,
                "type": "Mocha",
                "imageUrl": "https://example.com/images/mocha.jpg",
            },
            {
                "id": 6,
                "type": "Macchiato",
                "imageUrl": "https://example.com/images/macchiato.jpg",
            },
            {
                "id": 7,
                "type": "Flat White",
                "imageUrl": "https://example.com/images/flat_white.jpg",
            },
        ]
    }
    return data


async def get_countries(req: Optional[object] = None) -> dict:
    # Add your countries data here
    data = {
        "countries": [
            {"id": 1, "name": "United States"},
            {"id": 2, "name": "Canada"},
            {"id": 3, "name": "United Kingdom"},
            {"id": 4, "name": "Australia"},
            {"id": 5, "name": "Germany"},
            {"id": 6, "name": "France"},
            {"id": 7, "name": "India"},
            {"id": 8, "name": "Japan"},
        ]
    }
    return data


async def get_regions(req: Optional[object] = None) -> dict:
    data = {
        "shopByRegion": [
            {"id": 1, "name": "Ethiopia"},
            {"id": 2, "name": "Colombia"},
            {"id": 3, "name": "Brazil"},
            {"id": 4, "name": "Vietnam"},
            {"id": 5, "name": "Jamaica"},
            {"id": 6, "name": "Guatemala"},
        ]
    }
    return data


async def get_random_product_detail():
    query = """SELECT * FROM Product ORDER BY RANDOM() LIMIT 1;"""
    row = await Database.fetchrow(query)
    return row
