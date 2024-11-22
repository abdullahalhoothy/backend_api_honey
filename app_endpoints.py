from backend_common.common_endpoints import app
from fastapi import Depends
from fastapi import FastAPI, File, UploadFile

from api_responses.configuration import configuration_response
from backend_common.auth import JWTBearer
from backend_common.database import Database
from backend_common.request_processor import request_handling
from database_transformations.product import (
    create_product_table,
    get_recommended_products,
    get_preference_product_detail,
    get_user_reviews,
    get_favorite_products,
    get_random_product_detail,
    get_coffee_bean_types,
    get_coffee_types,
    get_countries,
    get_regions
)

from api_responses.response_dtypes import (
    ProductDetail,
    Product,
    UserReviews,
    FavoriteProducts,
    CoffeeBeanResponse,
    CoffeeProductResponse,
    CountryResponse,
    RegionResponse
)


@app.on_event("startup")
async def startup_event():
    await create_product_table()
    await Database.create_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await Database.close_pool()


@app.get("/configuration", dependencies=[])
async def configuration():
    return await request_handling(None, None, None, None, configuration_response)


@app.get("/recommended_products", dependencies=[])
async def recommended_products():
    return await request_handling(None, None, None, get_recommended_products)


@app.get("/preference_product_detail", dependencies=[])
async def preference_product_detail():
    return await request_handling(
        None, None, ProductDetail, get_preference_product_detail
    )


@app.get("/find_your_new_favorite_product", dependencies=[])
async def find_your_new_favorite_product():
    return await request_handling(None, None, FavoriteProducts, get_favorite_products)


@app.get("/user_reviews", dependencies=[])
async def user_reviews():
    return await request_handling(None, None, UserReviews, get_user_reviews)


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    return await request_handling(None, None, None, get_random_product_detail)


@app.get("/coffee-bean-types", dependencies=[])
async def coffee_bean_types():
    return await request_handling(None, None, CoffeeBeanResponse, get_coffee_bean_types)

@app.get("/coffee-types", dependencies=[])
async def coffee_types():
    return await request_handling(None, None, CoffeeProductResponse, get_coffee_types)

@app.get("/countries", dependencies=[])
async def countries():
    return await request_handling(None, None, CountryResponse, get_countries)

@app.get("/regions", dependencies=[])
async def regions():
    return await request_handling(None, None, RegionResponse, get_regions)