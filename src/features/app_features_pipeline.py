# numpy and pandas for data manipulation
import numpy as np
import pandas as pd 
import os,sys
from src.logging.custom_logging import logger
from src.exceptions.custom_exception import CustomException
#from src.utils.feature_engineering import compute_ratio_columnwise
from src.utils.other_utils import read_yaml_file



def main():
    


config = read_yaml_file("src/config/config.yaml")

print(config['TARGET_COL'])

