from enum import Enum

class ResponceSegnal(Enum):

    FILE_VALIDATION_SUCCESS = "File validation successful."
    FILE_TYPE_NOT_SUPPORTED = "File type not supported."
    FILE_SIZE_EXCEEDS_MAX_SIZE = "File size exceeds the maximum allowed size."
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully."
    FILE_UPLOADED_FAILED = "File upload failed."
    
    PROCESSING_FAILED = "File processing failed."
    PROCESSING_SUCCESS = "File processed successfully."