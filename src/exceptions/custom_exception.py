import sys
from src.logging.custom_logging import logger

class CustomException(Exception):
    def __init__(self, error_message):
        self.error_message = error_message
        _,_,exc_traceback = sys.exc_info()
        self.lineno = exc_traceback.tb_lineno
        self.file_name = exc_traceback.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error: {self.error_message} at line number {self.lineno} in file {self.file_name}"
    

if __name__ == "__main__":
    try:
        logger.info("This is a test log")
        a=1/0
    except Exception as e:
        raise CustomException(e)
        #logger.logging.error("Custom Error")
        #logger.logging.exception(NetworkSecurityException(e, sys))


#
#