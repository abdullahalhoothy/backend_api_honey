import json

from pyparsing import removeQuotes

from backend_common.common_endpoints import app
from fastapi import Depends
from fastapi import FastAPI, File, UploadFile, Form

from api_responses.configuration import configuration_response
from backend_common.common_config import CONF
from backend_common.auth import JWTBearer
from backend_common.database import Database
from backend_common.request_processor import request_handling
from backend_common.gbucket import upload_file_to_google_cloud_bucket
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
    get_regions,
    get_product_filters,
    get_filtered_products,
    get_single_user_review,
    insert_product_in_db
)

from api_responses.response_dtypes import (
    ProductDetail,
    Product,
    UserReviews,
    FavoriteProducts,
    CoffeeBeanResponse,
    CoffeeProductResponse,
    CountryResponse,
    RegionResponse,
    CoffeeDataResponse,
    ProductFiltersRequest,
    UserReviewRequest,
    SingleUserReview,
    UserReviewsRequest
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


@app.post("/user_reviews", dependencies=[])
async def user_reviews(request: UserReviewsRequest):
    return await request_handling(request, UserReviewsRequest, UserReviews, get_user_reviews)


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

@app.post("/product-filters", dependencies=[])
async def product_filters(request: ProductFiltersRequest):
    return await request_handling(request, ProductFiltersRequest, CoffeeDataResponse, get_product_filters)

@app.post("/filtered-products", dependencies=[])
async def filtered_products(request: ProductFiltersRequest):
    return await request_handling(request, ProductFiltersRequest, ProductDetail, get_filtered_products)

@app.post("/user-review", dependencies=[])
async def user_review(request: UserReviewRequest):
    return await request_handling(request, UserReviewRequest, SingleUserReview, get_single_user_review)


@app.post("/full-product/")
async def upload_image(product_front_image: UploadFile, product_back_image: UploadFile = File(...),
                       req : str = Form(...)):
    # Upload front_image to Google Cloud Storage
    req = json.loads(req)
    Product(**req)
    front_image_url = upload_file_to_google_cloud_bucket(product_front_image)
    back_image_url = upload_file_to_google_cloud_bucket(product_back_image)
    # Save metadata and URLs to the database
    req['additionalDetail'].update(productFrontImageUrl=front_image_url, productBackImageUrl=back_image_url, )
    req['userrating'] = json.dumps(req['userrating'])
    req['additionalDetail'] = json.dumps(req['additionalDetail'])
    return await request_handling(req, None, None, insert_product_in_db)


