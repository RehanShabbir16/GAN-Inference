from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import logging
from ..config.config import Config
from ..services.model_service import ModelService

app = FastAPI()
logger = logging.getLogger(__name__)


class TransformRequest(BaseModel):
    drive_link: str


def get_config():
    return Config.load()


def get_model_service(config: Config = Depends(get_config)):
    return ModelService(config)


@app.post("/api/v1/transform")
async def transform_data(
    request: TransformRequest,
    service: ModelService = Depends(get_model_service),
):
    try:
        result = service.process_data(request.drive_link)

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        return result
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
