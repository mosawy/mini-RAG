import os
from fastapi import APIRouter , Depends , UploadFile , status
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from controllers import DataController 
import aiofiles
from models import ResponceSegnal
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(
                        project_id:str,file:UploadFile,
                        app_settings : Settings = Depends(get_settings)
                    ):

    data_controller = DataController()
    # validate file properties
    is_valid , resalt_segnal = data_controller.validate_uploaded_file(file= file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "segnal":resalt_segnal
            }
        )

    file_path , file_id = data_controller.generate_unique_filepath(
        orginal_filename=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_DEFULT_CHUNK_SIZE):  # Read file in chunks
                await out_file.write(chunk)  # Write chunk to the destination file
    except Exception as e:
        
        logger.error(f"File upload failed: {e}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "segnal":ResponceSegnal.FILE_UPLOAD_FAILED.value
            }
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "segnal":ResponceSegnal.FILE_UPLOADED_SUCCESSFULLY.value,
            "file_id":file_id
        }
    )

