from typing import Optional
import json
from backend_common.database import Database


schema = {
    "id": "TEXT PRIMARY KEY",
    "productName": "varchar(70)",
    "productDescription": "text",
    "tagline": "text",
    "productUrl": "varchar(500)",
    "averageRating": "varchar(10)",
    "totalRatings": "varchar(10)",
    "discountedPrice": "varchar(10)",
    "discountPercentage": "varchar(10)",
    "originalPrice": "varchar(10)",
    "city": "varchar(30)",
    "country": "varchar(30)",
    "countryFlagUrl": "varchar(500)",
    "userRating": "JSONB"
}

sample_data = {
  "responseCode": 200,
  "data": {
    "justForYou": {
      "id": "66faa130bedf3403197df77c",
      "productName": "Wildflower Honey",
      "productDescription": "asdfasdf",
      "tagline": "A good match for your taste",
      "productUrl": "https://bestbees.com/2022/10/26/types-of-honey/",
      "averageRating": "4.5",
      "totalRatings": "884",
      "discountedPrice": "32.99",
      "discountPercentage": "32%",
      "originalPrice": "50",
      "city": "Barolo",
      "country": "Italy",
      "countryFlagUrl": "https://imageicon",
      "userRating": '''{
        "rating": "4.3",
        "review": "50",
        "userName": "Barolo",
        "userProfileImageUrl": "Italy"
      }'''
    },
    # "bestPick": {
    #   "id": "66faa130bedf3403197df77c",
    #   "productName": "Wildflower Honey",
    #   "productDescription": "asdfasdf",
    #   "tagline": "A good match for your taste",
    #   "productUrl": "https://bestbees.com/2022/10/26/types-of-honey/",
    #   "averageRating": "4.5",
    #   "totalRatings": "884",
    #   "discountedPrice": "32.99",
    #   "discountPercentage": "32%",
    #   "originalPrice": "50",
    #   "city": "Barolo",
    #   "country": "Italy",
    #   "countryFlagUrl": "https://imageicon",
    #   "userRating": {
    #     "rating": "4.3",
    #     "review": "50",
    #     "userName": "Barolo",
    #     "userProfileImageUrl": "Italy"
    #   }
    # },
  },
"bannerImageUrl": "https://"
    ,
  "message": "Honey list fetched successfully"
}


async def create_product_table() -> None:
    # Create table if it doesn't exist

    columns = ''.join([f'{k} {v},' for k, v in schema.items()]).strip(',')
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS Product (
            {columns}
    );
    """
    await Database.execute(create_table_query)
    columns = ''.join([f'{k}, ' for k in schema.keys()]).rstrip(', ')
    for entries in sample_data['data'].values():
        await insert_product(columns, entries)

async def insert_product(columns: str, entries: dict) -> None:
    # Create table if it doesn't exist
    placeholders = ''.join([f'${i + 1}, ' for i in range(len(entries.values()))]).rstrip(', ')
    entry = [f'{v}' for v in entries.values()]
    query = f"""
        INSERT INTO Product ({columns})  
            VALUES({placeholders})
        On CONFLICT(id) DO NOTHING;
        """
    await Database.execute(query, *entry)


async def get_all_products(req: Optional[object]) -> dict:
    # Create table if it doesn't exist
    query = f"""SELECT * FROM Product;"""
    row = dict((await Database.fetchrow(query)).items())
    row['userrating'] = json.loads(row['userrating'])
    data = {
        'justForYou': row,
        'bestPick': row
    }
    return  {
        "responseCode": 200,
        "message": "Returned recommended products.",
        "data": data
    }
