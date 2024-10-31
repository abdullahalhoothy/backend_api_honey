from backend_common.common_endpoints import app
from fastapi import Depends

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
)

from api_responses.response_dtypes import (
    ProductDetail,
    Product,
    UserReviews,
    FavoriteProducts,
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
