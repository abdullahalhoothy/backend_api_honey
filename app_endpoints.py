from backend_common.common_endpoints import app
from fastapi import Depends

from api_responses.configuration import configuration_response
from backend_common.auth import JWTBearer
from backend_common.database import Database
from backend_common.dtypes.response_dtypes import ConfigurationResponse, RecommendedProducts
from backend_common.request_processor import request_handling
from database_transformations.product import create_product_table, get_all_products


@app.on_event("startup")
async def startup_event():
    await create_product_table()
    await Database.create_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await Database.close_pool()


@app.get('/index2', dependencies=[Depends(JWTBearer())])
# this needs to use request_handling
def index():
    return {'message': 'Hello World'}


@app.get('/configuration', dependencies=[])
async def configuration():
    return await request_handling(None, None, ConfigurationResponse,
                     None, configuration_response)

@app.get('/recommended_products', dependencies=[])
async def recommended_products():
    return await request_handling(None, None, RecommendedProducts,
                                  get_all_products)
