from typing import Optional
import json
from backend_common.database import Database
from database_transformations.product_schema import SCHEMA
from database_transformations.sample_product_data import SAMPLE_PRODUCT



async def create_product_table() -> None:
    # Create table if it doesn't exist

    columns = ''.join([f'{k} {v},' for k, v in SCHEMA.items()]).strip(',')
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS Product (
            {columns}
    );
    """
    await Database.execute(create_table_query)
    columns = ''.join([f'{k}, ' for k in SCHEMA.keys()]).rstrip(', ')
    await insert_product(columns)

async def insert_product(columns: str) -> None:
    # Create table if it doesn't exist
    entries = SAMPLE_PRODUCT
    placeholders = ''.join([f'${i + 1}, ' for i in range(len(entries[0].values()))]).rstrip(', ')
    entries = [list(entry.values()) for entry in entries]
    query = f"""
        INSERT INTO Product ({columns})  
            VALUES({placeholders})
        On CONFLICT(id) DO NOTHING;
        """
    await Database.execute_many(query, entries)


async def get_recommended_products(req: Optional[object]) -> dict:
    # Create table if it doesn't exist
    query = f"""
    SELECT * FROM Product
    WHERE id='66faa130bedf3403197df77c'            
    ;"""
    row = dict((await Database.fetchrow(query)).items())
    row['userrating'] = json.loads(row['userrating'])
    data = {
        'justForYou': row,
        'bestPick': row,
        'bannerImageUrl': "https://"
    }
    return  data

async def get_preference_product_detail(req: Optional[object]) -> dict:
    # Create table if it doesn't exist
    query = f"""
    SELECT * FROM Product
    WHERE id='66faa130bedf3403197df77d'            
    ;"""
    row = dict((await Database.fetchrow(query)).items())
    row['userrating'] = json.loads(row['userrating'])
    return  {
        'product': row
    }
