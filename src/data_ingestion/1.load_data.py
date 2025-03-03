import os
import shutil
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
#from kaggle.api.kaggle_api_extended import KaggleApi
import kagglehub
from src.logging.custom_logging import logger
from src.exceptions.custom_exception import CustomException


# Get Kaggle Credentials
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")

if KAGGLE_USERNAME is None or KAGGLE_KEY is None:
    raise ValueError("You need to set your Kaggle username and key in the .env file")


logger.info("Authenticated with Kaggle")

# Define the dataset
home_credit_default_risk_path = kagglehub.competition_download('home-credit-default-risk')

# Download and extract the dataset

download_path = 'data/raw'
print(home_credit_default_risk_path)

# Move the downloaded files to the custom directory
for file in os.listdir(home_credit_default_risk_path):
    shutil.move(os.path.join(home_credit_default_risk_path, file), os.path.join(download_path, file))

print(f"Dataset downloaded to: {download_path}")
logger.info("Downloaded and extracted the dataset")





