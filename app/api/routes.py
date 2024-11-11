from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import logging
from ..config.config import Config
from ..services.model_service import ModelService

app = FastAPI()
logger = logging.getLogger(__name__)


class InverseTransformRequest(BaseModel):
    transformed_file_path: str


class TransformRequest(BaseModel):
    drive_link: str


def get_config():
    return Config.load()


def get_model_service(config: Config = Depends(get_config)):
    return ModelService(config)

service = get_model_service(get_config())


@app.post("/api/v1/transform")
async def transform_data(
    request: TransformRequest,
):
    try:
        result = service.process_data(request.drive_link)

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        return result
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/inverse_transform")
async def inverse_transform_data(
    request: InverseTransformRequest,
):
    try:
        result = service.inverse_data(request.transformed_file_path)

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        return result
    except ValueError as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
