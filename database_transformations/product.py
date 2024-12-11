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
        On CONFLICT(product_id) DO NOTHING;
        """
    await Database.execute_many(query, entries)

async def insert_product_in_db(req: dict) -> dict:
    # Create table if it doesn't exist
    product = req
    columns, placeholders, values = '', '', []
    for index, name in enumerate(product.keys(), start=1):
        placeholders += f"${index}, "
        columns += f"{name}, "
        values.append(product[name])
    placeholders = placeholders.rstrip(", ")
    columns = columns.rstrip(", ")
    query = f"""
        INSERT INTO "schema_marketplace".products ({columns})  
            VALUES({placeholders})
        On CONFLICT(product_id) DO NOTHING;
        """
    await Database.execute_many(query, [values])
    return {}


async def get_recommended_products(req: Optional[object] = None) -> dict:
    query = f"""
    SELECT * FROM "schema_marketplace".products
    ;"""
    product_info = dict((await Database.fetchrow(query)).items())
    product_info["userrating"] = json.loads(product_info["userrating"])
    product_info["userrating"]["review_id"] = "3422"

    # fetch banner images
    query_banner = """SELECT * FROM "schema_app_generic".banners
    ORDER BY RANDOM()
    LIMIT 1;"""
    data = await Database.fetchrow(query_banner)
    banner_item = dict(data.items())
    image_banner_url = banner_item["url"]

    data = {
        "justForYou": product_info,
        "bestPick": product_info,
        "bannerImageUrl": image_banner_url,
    }
    return data


async def get_preference_product_detail():
    query = """SELECT * FROM "schema_marketplace".products;"""
    rows = await Database.fetch(query)
    products = list(map(dict, rows))
    for product in products:
        product["userrating"] = json.loads(product["userrating"])
        product["userrating"]["review_id"] = "3422"
    return {"products": products}


async def get_favorite_products(req: Optional[object] = None) -> List[Dict]:

    ## Waiting for Logic
    data = {
        "products": [
            {"product_id": 101, "name": "Espresso", "searchType": "scan"},
            {"product_id": 102, "name": "Cappuccino", "searchType": "search"},
            {"product_id": 103, "name": "Latte", "searchType": "scan"},
            {"product_id": 104, "name": "Americano", "searchType": "search"},
        ]
    }
    return data


async def get_user_reviews(req: Optional[object] = None) -> dict:
    data = {
        "reviews": [
            {
                "review_id": 201,
                "name": "John Doe",
                "userProfileImageUrl": "https://example.com/images/john_doe.jpg",
                "description": "Great product, highly recommend!",
                "averageRating": 4.5,
                "totalRatings": 120,
                "time": "2 months ago",
            },
            {
                "review_id": 202,
                "name": "Jane Smith",
                "userProfileImageUrl": "https://example.com/images/jane_smith.jpg",
                "description": "Good quality, but a bit overpriced.",
                "averageRating": 3.8,
                "totalRatings": 85,
                "time": "2 months ago",
            },
            {
                "review_id": 203,
                "name": "Alex Johnson",
                "userProfileImageUrl": "https://example.com/images/alex_johnson.jpg",
                "description": "Exceeded my expectations. Will buy again!",
                "averageRating": 4.9,
                "totalRatings": 200,
                "time": "2 months ago",
            },
            {
                "review_id": 204,
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
                "product_id": 1,
                "type": "Espresso",
                "imageUrl": "hhttps://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/9.jpeg",
            },
            {
                "product_id": 2,
                "type": "Latte",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/9.jpeg",
            },
            {
                "product_id": 3,
                "type": "Cappuccino",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "product_id": 4,
                "type": "Americano",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "product_id": 5,
                "type": "Mocha",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "product_id": 6,
                "type": "Macchiato",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/8.jpeg",
            },
            {
                "product_id": 7,
                "type": "Flat White",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/8.jpeg",
            },
        ]
    }
    return data


async def get_countries(req: Optional[object] = None) -> dict:
    # Add your countries data here
    data = {
        "countries": [
            {
                "id": 1,
                "name": "United States",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/9.jpeg",
            },
            {
                "id": 2,
                "name": "Canada",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/9.jpeg",
            },
            {
                "id": 3,
                "name": "United Kingdom",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "id": 4,
                "name": "Australia",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "id": 5,
                "name": "Germany",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "id": 6,
                "name": "France",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "id": 7,
                "name": "India",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/8.jpeg",
            },
            {
                "id": 8,
                "name": "Japan",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/8.jpeg",
            },
        ]
    }
    return data


async def get_regions(req: Optional[object] = None) -> dict:
    data = {
        "shopByRegion": [
            {
                "id": 1,
                "name": "Ethiopia",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/8.jpeg",
            },
            {
                "id": 2,
                "name": "Colombia",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/8.jpeg",
            },
            {
                "id": 3,
                "name": "Brazil",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "id": 4,
                "name": "Vietnam",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "id": 5,
                "name": "Jamaica",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/10.jpeg",
            },
            {
                "id": 6,
                "name": "Guatemala",
                "imageUrl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_app_generic/banners/9.jpeg",
            },
        ]
    }
    return data


async def get_random_product_detail():
    query = """SELECT * FROM Product ORDER BY RANDOM() LIMIT 1;"""
    row = await Database.fetchrow(query)
    return row


async def get_product_filters(req: Optional[object] = None) -> dict:
    data = {
        "coffeeData": {
            "coffeeTypes": [
                {"id": 1, "name": "Espresso", "count": 40},
                {"id": 2, "name": "Latte", "count": 40},
                {"id": 3, "name": "Cappuccino", "count": 40},
                {"id": 4, "name": "Americano", "count": 40},
            ],
            "coffeeBeanTypes": [
                {"id": 1, "name": "Arabica", "count": 40},
                {"id": 2, "name": "Robusta", "count": 40},
                {"id": 3, "name": "Liberica", "count": 40},
                {"id": 4, "name": "Excelsa", "count": 40},
            ],
            "countries": [
                {"id": 1, "name": "Brazil", "count": 50},
                {"id": 2, "name": "Colombia", "count": 40},
                {"id": 3, "name": "Ethiopia", "count": 30},
                {"id": 4, "name": "Vietnam", "count": 35},
            ],
            "regions": [
                {"id": 1, "name": "South America", "count": 70},
                {"id": 2, "name": "Africa", "count": 50},
                {"id": 3, "name": "Asia", "count": 40},
            ],
            "coffeeStyles": [
                {"id": 1, "name": "Hot", "count": 40},
                {"id": 2, "name": "Cold", "count": 40},
                {"id": 3, "name": "Iced", "count": 40},
                {"id": 4, "name": "Blended", "count": 40},
            ],
            "sizes": [
                {"id": 1, "sizeValue": 0.375, "count": 40},
                {"id": 2, "sizeValue": 0.75, "count": 40},
                {"id": 3, "sizeValue": 1.0, "count": 40},
            ],
        }
    }
    return data


async def get_filtered_products(req: Optional[object] = None) -> dict:
    data = {
        "products": [
            {
                "product_id": "cb0545375af050c698f8cc98ad5f0628",
                "name": "Nescafe Classic Instant Coffee Jar 190g",
                "description": "Experience a distinct and premium coffee taste with this imported soluble coffee powder. Crafted from the finest blend of Robusta and Arabica beans, each cup offers a rich and smooth flavor, expertly prepared to make your coffee moments truly special. The specially designed glass jar ensures that your Nescafe Gold stays fresh and flavorful to the last drop, preserving its aroma and taste for a consistently satisfying experience.",
                "tagline": "Features:\nFlavor Profile: Rich and robust flavor with a smooth finish, perfect for any time of day.\nInstant Convenience: Quickly dissolves in hot water, allowing for a fast and easy coffee preparation.\nQuality Beans: Made from high-quality coffee beans, expertly roasted to deliver a classic coffee taste.\nVersatile Use: Can be enjoyed as a hot beverage or used as a base for cold coffee drinks, desserts, and recipes.\n\nBrewing Instructions:\nMeasure: Use 1-2 teaspoons of instant coffee per cup (200ml) of hot water, adjusting according to your taste preference.\nMix: Stir the coffee granules in hot water until fully dissolved.\nServe: Enjoy as is, or customize with milk, sugar, or flavored syrups as desired.\n\nStorage:\nKeep in a cool, dry place and ensure the jar is tightly sealed after use to maintain freshness.\n",
                "producturl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/0.png",
                "imageurl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/1.png",
                "averagerating": "4.2",
                "totalratings": "500",
                "discountedprice": "25.457500648498534",
                "discountpercentage": "15%",
                "originalprice": "29.95",
                "city": "Barolo",
                "country": "Italy",
                "userrating": {
                    "review_id": "3422",
                    "rating": "4.0",
                    "review": "Good product",
                    "username": "Default Reviewer",
                    "description": "Clear deep ruby in color with medium intensity",
                    "userimageurl": "default_image_url",
                },
            },
            {
                "product_id": "a848b13fa88a4cf5fb96e9e2a1827f0a",
                "name": "Nescafe Gold Decaf Instant Coffee Jar 95g",
                "description": "Enjoy the rich, smooth taste of Nescafe Gold without the caffeine. Made from carefully selected Arabica and Robusta beans, this premium decaf blend delivers the same great flavor you love. The 95g jar ensures freshness and convenience, perfect for a relaxing cup of coffee at any time of the day. Ideal for those seeking a high-quality coffee experience without the caffeine kick",
                "tagline": "Features:\nDecaffeinated: Crafted using a special decaffeination process to retain the rich flavor while removing caffeine.\nRich Flavor: Offers a smooth and well-balanced taste profile with a hint of sweetness, ideal for coffee lovers looking for a caffeine-free option.\nInstant Convenience: Easily dissolves in hot water, providing a quick and hassle-free coffee experience.\nVersatile Use: Great for hot or cold coffee drinks, and can also be used in various recipes for desserts or baking.\n\nBrewing Instructions:\nMeasure: Use 1-2 teaspoons of Nescafe Gold Decaf per cup (200ml) of hot water, adjusting according to taste.\nMix: Stir the granules into hot water until fully dissolved.\nServe: Enjoy as is, or enhance with milk, sugar, or flavorings as desired.\n\nStorage:\nStore in a cool, dry place and keep the jar tightly sealed after use to preserve freshness.\n",
                "producturl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/10.png",
                "imageurl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/100.png",
                "averagerating": "4.2",
                "totalratings": "500",
                "discountedprice": "33.95750064849853",
                "discountpercentage": "15%",
                "originalprice": "39.95",
                "city": "Barolo",
                "country": "Italy",
                "userrating": {
                    "review_id": "3422",
                    "rating": "4.0",
                    "review": "Good product",
                    "username": "Default Reviewer",
                    "description": "Clear deep ruby in color with medium intensity",
                    "userimageurl": "default_image_url",
                },
            },
            {
                "product_id": "4ed95bc7fcd498bfa70ee0205afc3aae",
                "name": "Nescafe 3in1 Instant Coffee Mix Stick 20g (30+5 Sticks)",
                "description": "Nescafe Instant Coffee Sticks are convenient single-serve packets of instant coffee, perfect for on-the-go coffee lovers. Each stick contains a blend of rich coffee that delivers the classic Nescafe taste with ease.\n",
                "tagline": "Features:\nSingle-Serve Convenience: Each stick contains just the right amount of instant coffee for one cup, making it easy to enjoy coffee anywhere.\nRich Flavor: Delivers the familiar smooth and aromatic taste that Nescafe is known for.\nQuick Preparation: Simply mix with hot water for an instant coffee experience in seconds.\nVersatile: Ideal for home, work, travel, or outdoor activities.\n\nBrewing Instructions:\nOpen: Tear open a stick.\nMix: Empty the contents into a cup of hot water (about 200 ml).\nStir: Mix well until the coffee dissolves.\nServe: Enjoy plain or customize with milk, sugar, or your favorite flavors.\n\nStorage:\nStore in a cool, dry place. Reseal the box after use to maintain freshness.\n",
                "producturl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/101.png",
                "imageurl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/102.png",
                "averagerating": "4.2",
                "totalratings": "500",
                "discountedprice": "48.95000076293945",
                "discountpercentage": "32%",
                "originalprice": "54.45",
                "city": "Barolo",
                "country": "Italy",
                "userrating": {
                    "review_id": "3422",
                    "rating": "4.0",
                    "review": "Good product",
                    "username": "Default Reviewer",
                    "description": "Clear deep ruby in color with medium intensity",
                    "userimageurl": "default_image_url",
                },
                "additionalDetail": {
                    "sellerRating": {
                        "userName": "Michael Millder",
                        "userRatings": 328
                    },
                    "summary": {
                        "highlights": [
                            "Great value for money, similar vivi usually costs about 2 times as much",
                            "Among top 2% of all vivi in the world"
                        ],
                        "facts": "100% hygienic"
                    },
                    "tasteCharacteristics": {
                        "totalReviews": 2563,
                        "characteristics": {
                            "Characteristic_1": {
                                "start": "Light",
                                "percentage": "60%",
                                "end": "Bold"
                            },
                            "Characteristic_2": {
                                "start": "Small",
                                "percentage": "60%",
                                "end": "Large"
                            },
                            "Characteristic_3": {
                                "start": "Dim",
                                "percentage": "60%",
                                "end": "Bright"
                            },
                            "Characteristic_4": {
                                "start": "Small",
                                "percentage": "60%",
                                "end": "Large"
                            }
                        }
                    },
                    "whatPeopleTalkAbout": {
                        "talkTags_1": [
                            "Citrus, lemon, grapefruit",
                            "57 mentions of citrus fruit notes"
                        ],
                        "talkTags_2": [
                            "Peach, apricot, pear",
                            "37 mentions of tree fruit notes"
                        ],
                        "talkTags_3": [
                            "Stone, Honey, minerals",
                            "25 mentions of earthy notes"
                        ]
                    },
                    "reviews": {
                        "helpful": [
                            {
                                "consumerName": "John White",
                                "outOf5Rating": "4.9",
                                "description": ""
                            }
                        ],
                        "recent": [
                            {
                                "consumerName": "John White",
                                "outOf5Rating": "4.9",
                                "description": ""
                            }
                        ]
                    },
                    "productRanking": [
                        {
                            "name": "World",
                            "percentage": "70%,"
                        },
                        {
                            "name": "Nepal Valley",
                            "percentage": "70%,"
                        }
                    ],
                    "productOriginStory": "California is known primarily for its cabinet and chardonnay but they are also producing some really lovely savonian ....",
                    "pairsWellWith": [
                        "ShellFish",
                        "Vegetarian",
                        "Goat's Milk Cheese",
                        "Fettuccine Alfredo"
                    ],
                    "producerDetails": {
                        "producerType": "Coffee",
                        "producerName": "Borgogno",
                        "numProducts": "39",
                        "cityOverallRanking": "4.5",
                        "cityTotalRating": "86944",
                        "cityName": "Piemonte",
                        "countryName": "Italy",
                        "producerAddress": "277 bedfrord ave broklyne Ny 11211, usa"
                    },
                    "vintageComparison": {
                        "recent": {
                            "2020": {
                                "ratingValue": "4.0",
                                "totalRatings": "344"
                            }
                        },
                        "bestPrice": {},
                        "topRating": {}
                    }
                }
            },
            {
                "product_id": "2b579cbecdccb3a34350514ba5338252",
                "name": "Nescafe 2in1 Classic 11.7g, Pack of 30",
                "description": "Nescafé 2in1 Classic offers a convenient blend of rich instant coffee and creamer in a single sachet. Its perfect for those who enjoy a quick, easy, and balanced coffee experience without the need for added sugar.",
                "tagline": "Brand: Nescafe\nProduct Name: 2in1 Classic\nPackaging: Pack of 30 sachets\nSachet Size: 11.7g each\nIngredients: Instant coffee, sugar, and non-dairy creamer.\nFlavor Profile:\nSmooth and balanced with a rich coffee taste.\nSweetened to provide a delightful flavor without any additional ingredients.\nPreparation Method:\nSimply empty the sachet into a cup.\nAdd hot water, stir well, and enjoy.\nConvenience:\nIdeal for on-the-go, at the office, or at home.\nNo need for measuring or additional ingredients, making it perfect for busy lifestyles.",
                "producturl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/103.png",
                "imageurl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/104.jpg",
                "averagerating": "4.2",
                "totalratings": "500",
                "discountedprice": "29.707500648498534",
                "discountpercentage": "15%",
                "originalprice": "34.95",
                "city": "Barolo",
                "country": "Italy",
                "userrating": {
                    "review_id": "3422",
                    "rating": "4.0",
                    "review": "Good product",
                    "username": "Default Reviewer",
                    "description": "Clear deep ruby in color with medium intensity",
                    "userimageurl": "default_image_url",
                },
            },
            {
                "product_id": "744444889fbb91770001b4c6605497e1",
                "name": "Nescafe Gold Dark Roast Jar 190g",
                "description": "Nescafé Gold Dark Roast is crafted from a premium blend of high-quality, dark-roasted Arabica and Robusta coffee beans. This instant coffee offers an intense, rich, and full-bodied flavor with a robust aroma, perfect for those who enjoy a deep coffee experience. Its designed to deliver a superior taste with a refined finish, making it ideal for a premium coffee moment at home.",
                "tagline": "Brand: Nescafe\nProduct Name: Gold Dark Roast\nPackaging: Jar\nNet Weight: 190g\nIngredients: Instant coffee.\nFlavor Profile:\nIntense and bold with a deep roasted flavor.\nSmooth texture with a rich aroma that enhances the coffee experience.\nPreparation Method:\nAdd 1-2 teaspoons of coffee to a cup.\nPour hot water and stir until dissolved. Enjoy your coffee!\nVersatility:\nPerfect for making classic coffee or as a base for various coffee recipes.\nCan be enjoyed black or with milk and sugar to taste.",
                "producturl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/104.png",
                "imageurl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/105.png",
                "averagerating": "4.2",
                "totalratings": "500",
                "discountedprice": "43.30750064849853",
                "discountpercentage": "15%",
                "originalprice": "50.95",
                "city": "Barolo",
                "country": "Italy",
                "userrating": {
                    "review_id": "3422",
                    "rating": "4.0",
                    "review": "Good product",
                    "username": "Default Reviewer",
                    "description": "Clear deep ruby in color with medium intensity",
                    "userimageurl": "default_image_url",
                },
            },
            {
                "product_id": "e81bbd7cd6bb6dd0fa6a06ec69ccc144",
                "name": "Nescafe Classic Instant Coffee Jar 95g",
                "description": "Nescafé Classic Instant Coffee offers a rich, robust, and aromatic coffee experience, made from 100% pure coffee beans. Carefully selected and roasted to perfection, this instant coffee is ideal for those who enjoy a bold and strong flavor. It is designed to deliver a consistent and rich cup of coffee with a smooth finish, providing the perfect start to your day or a refreshing break anytime.\n",
                "tagline": "Brand: Nescafe\nProduct Name: Classic Instant Coffee\nPackaging: Jar\nNet Weight: 95g\nIngredients: 100% instant coffee.\nFlavor Profile:\nClassic and balanced flavor with a smooth finish.\nRich aroma that awakens the senses.\nPreparation Method:\nAdd 1-2 teaspoons of instant coffee to a cup.\nPour hot water and stir well until dissolved. Enjoy your coffee!\nVersatility:\nIdeal for everyday coffee consumption.\nCan be enhanced with milk, cream, or sugar according to personal preference.",
                "producturl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/106.png",
                "imageurl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/109.png",
                "averagerating": "4.2",
                "totalratings": "500",
                "discountedprice": "17.425",
                "discountpercentage": "15%",
                "originalprice": "20.5",
                "city": "Barolo",
                "country": "Italy",
                "userrating": {
                    "review_id": "3422",
                    "rating": "4.0",
                    "review": "Good product",
                    "username": "Default Reviewer",
                    "description": "Clear deep ruby in color with medium intensity",
                    "userimageurl": "default_image_url",
                },
            },
        ]
    }
    return data


async def get_single_user_review(req: Optional[object] = None) -> dict:
    data = {
        "product_id": "e81bbd7cd6bb6dd0fa6a06ec69ccc144",
        "name": "Nescafe Classic Instant Coffee Jar 95g",
        "description": "Nescafé Classic Instant Coffee offers a rich, robust, and aromatic coffee experience, made from 100% pure coffee beans. Carefully selected and roasted to perfection, this instant coffee is ideal for those who enjoy a bold and strong flavor. It is designed to deliver a consistent and rich cup of coffee with a smooth finish, providing the perfect start to your day or a refreshing break anytime.\n",
        "tagline": "Brand: Nescafe\nProduct Name: Classic Instant Coffee\nPackaging: Jar\nNet Weight: 95g\nIngredients: 100% instant coffee.\nFlavor Profile:\nClassic and balanced flavor with a smooth finish.\nRich aroma that awakens the senses.\nPreparation Method:\nAdd 1-2 teaspoons of instant coffee to a cup.\nPour hot water and stir well until dissolved. Enjoy your coffee!\nVersatility:\nIdeal for everyday coffee consumption.\nCan be enhanced with milk, cream, or sugar according to personal preference.",
        "producturl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/106.png",
        "imageurl": "https://storage.googleapis.com/vivi_app/postgreSQL/dbo-coffee/raw_schema_marketplace/product_images/109.png",
        "averagerating": "4.2",
        "totalratings": "500",
        "discountedprice": "17.425",
        "discountpercentage": "15%",
        "originalprice": "20.5",
        "city": "Barolo",
        "country": "Italy",
        "userrating": {
            "review_id": "3422",
            "rating": "4.0",
            "review": "Good product",
            "username": "Default Reviewer",
            "description": "Clear deep ruby in color with medium intensity",
            "userimageurl": "default_image_url",
        },
    }
    return data
