from enum import Enum

class ResponceSegnal(Enum):

    FILE_VALIDATION_SUCCESS = "File validation successful."
    FILE_TYPE_NOT_SUPPORTED = "File type not supported."
    FILE_SIZE_EXCEEDS_MAX_SIZE = "File size exceeds the maximum allowed size."
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully."
    FILE_UPLOADED_FAILED = "File upload failed."
    
    PROCESSING_FAILED = "File processing failed."
    PROCESSING_SUCCESS = "File processed successfully."

    NO_FILES_ERROR = "No files found."
    FILE_ID_ERROR = "File ID error."

    PROJECT_NOT_FOUND = "Project not found."
    INSERT_INTO_VECTOR_DB_FAILED = "Failed to insert data into vector database."
    INSERT_INTO_VECTOR_DB_SUCCESS = "Data inserted into vector database successfully."
    VECTOR_DB_COLLECTION_RETRIEVED_SUCCESS = "Vector database collection information retrieved successfully."
    VECTOR_SEARCH_SUCCESS = "Vector database search completed successfully."
    VECTOR_SEARCH_FAILED = "Vector database search failed."