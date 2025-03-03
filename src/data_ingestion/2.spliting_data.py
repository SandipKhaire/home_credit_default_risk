# numpy and pandas for data manipulation
import numpy as np
import pandas as pd 
import os
from sklearn.model_selection import train_test_split
from src.logging.custom_logging import logger


def stratified_split_and_save(df, target_column, train_file_name, test_file_name, path, test_size=0.3, random_state=42):
    """
    Perform a stratified split on the DataFrame based on the target column and save the splits to files.

    Parameters:
    - df: pandas DataFrame, the original dataset.
    - target_column: str, the name of the target column.
    - train_file_name: str, the name of the file to save the training data.
    - test_file_name: str, the name of the file to save the testing data.
    - path: str, the directory path where the files will be saved.
    - test_size: float, the proportion of the dataset to include in the test split (default is 0.3).
    - random_state: int, random seed for reproducibility (default is 42).
    """
    # Perform the stratified split
    train_df, test_df = train_test_split(
        df, 
        test_size=test_size, 
        stratify=df[target_column], 
        random_state=random_state
    )
    
    # Create the full file paths
    train_file_path = os.path.join(path, train_file_name)
    test_file_path = os.path.join(path, test_file_name)
    
    # Save the splits to files
    train_df.to_csv(train_file_path, index=False)
    test_df.to_csv(test_file_path, index=False)
    
    logger.info(f"Training data saved to {train_file_path}")
    logger.info(f"Testing data saved to {test_file_path}")

# Example usage
if __name__ == "__main__":
    # Load your DataFrame (replace this with your actual DataFrame loading code)
    df = pd.read_csv("./data/raw/application_train.csv")
    
    # Define the target column
    target_column = "TARGET"
    
    # Define the output filenames and path
    train_file_name = "app_train.csv"
    test_file_name = "app_test.csv"
    save_path = "./data/raw"  # Replace with your desired directory path
    
    # Perform the stratified split and save the files
    stratified_split_and_save(df, target_column, train_file_name, test_file_name, save_path)