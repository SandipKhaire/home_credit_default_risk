import yaml
from src.logging.custom_logging import logger
from src.exceptions.custom_exception import CustomException
import os,sys


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e) 