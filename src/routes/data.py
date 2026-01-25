import os
from urllib import request
from fastapi import APIRouter , Depends , UploadFile , status , Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from controllers import DataController , ProjectController , ProcessController
import aiofiles
from models import ResponceSegnal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunk
from models.ChunkModel import ChunkModel

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(
                        request:Request,
                        project_id:str,file:UploadFile,
                        app_settings : Settings = Depends(get_settings)
                    ):

    project_model = await ProjectModel.create_instance(
        request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

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


@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request, project_id:str,process_request:ProcessRequest):

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(
        request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )


    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "segnal":ResponceSegnal.PROCESSING_FAILED.value
            }
        )
    
    file_chunks_recorded = [
        DataChunk(
            chunk_text = chunk.page_content,
            chunk_metadata = chunk.metadata,
            chunk_order=i +1,
            chunk_project_id=project.id

        )
        for i, chunk in enumerate(file_chunks)
    ]

    chunk_model = await ChunkModel.create_instance(
        request.app.db_client
    )
    if do_reset:

        deleted_count = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

        logger.info(f"Deleted {deleted_count} chunks for project_id: {project_id}")

    no_records = await chunk_model.insert_many_chunks(
        chunks=file_chunks_recorded
    )

    return JSONResponse(
        content={
            "segnal":ResponceSegnal.PROCESSING_SUCCESS.value,
            "inserted_chunks":no_records
        })