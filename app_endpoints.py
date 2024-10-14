from backend_common.common_endpoints import app
from fastapi import Depends
from backend_common.auth import JWTBearer

# fastpi there is add routes or make router instance??

@app.get('/index2', dependencies=[Depends(JWTBearer())])
# this needs to use request_handling
def index():
    return {'message': 'Hello World'}
