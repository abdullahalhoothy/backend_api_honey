from typing import Optional
import json
from backend_common.database import Database
from database_transformations.product_schema import SCHEMA
from database_transformations.sample_product_data import SAMPLE_PRODUCT


async def create_product_table() -> None:
    # Create table if it doesn't exist
    print("1")
    columns = "".join([f"{k} {v}," for k, v in SCHEMA.items()]).strip(",")
    print("1")
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS Product (
            {columns}
    );
    """

    print("1", create_table_query)
    await Database.execute(create_table_query)
    columns = "".join([f"{k}, " for k in SCHEMA.keys()]).rstrip(", ")
    await insert_product(columns)

    return


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
    rows = await Database.fetch(query)

    dict_data = [dict(row) for row in rows]

    for row in dict_data:
        row["userrating"] = json.loads(row["userrating"])

    return dict_data


async def get_preference_product_detail(req: Optional[object] = None) -> dict:
    # Create table if it doesn't exist
    query = f"""
    SELECT * FROM Product
    WHERE id='66faa130bedf3403197df77d'            
    ;"""

    row = await Database.fetchrow(query)

    dict_data = dict(row)

    dict_data["userrating"] = json.loads(dict_data["userrating"])

    return {"product": dict_data}
