from app_endpoints import app
import uvicorn
from backend_common.logger import logging


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
