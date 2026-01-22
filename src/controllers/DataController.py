from fileinput import filename
import os
from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import  UploadFile
from models import ResponceSegnal
import re

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # Convert MB to Bytes

    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponceSegnal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False , ResponceSegnal.FILE_SIZE_EXCEEDS_MAX_SIZE.value

        return True , ResponceSegnal.FILE_VALIDATION_SUCCESS.value
    
    def generate_unique_filepath(self,orginal_filename:str,project_id:str):
        
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        clean_file_name = self.get_clean_filename(orginal_filename=orginal_filename)

        new_file_path = os.path.join(
                project_path,
                f"{random_key}_{clean_file_name}"
            )
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                f"{random_key}_{clean_file_name}"
            )
        return new_file_path , random_key + "_" + clean_file_name
    

    def get_clean_filename(self,orginal_filename:str):
        
        # Remove any unwanted characters from the filename
        clean_file_name = re.sub(r'[^\w.]','', orginal_filename.strip())
        clean_file_name = clean_file_name.replace(" ","_")
        
        return clean_file_name
