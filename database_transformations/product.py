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
    # Create table if it doesn't exist
    query = f"""
    SELECT * FROM Product           
    ;"""
    row = dict((await Database.fetchrow(query)).items())
    row["userrating"] = json.loads(row["userrating"])
    data = {"justForYou": row, "bestPick": row, "bannerImageUrl": "https://"}
    return data


async def get_preference_product_detail(req: Optional[object] = None) -> dict:
    # Create table if it doesn't exist
    query = f"""
    SELECT * FROM Product          
    ;"""

    row = await Database.fetchrow(query)

    dict_data = dict(row)

    dict_data["userrating"] = json.loads(dict_data["userrating"])

    return {"product": dict_data}


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
