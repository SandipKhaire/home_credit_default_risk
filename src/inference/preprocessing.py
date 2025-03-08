import yaml
import numpy as np
import pandas as pd
from src.logging.custom_logging import logger
from src.exceptions.custom_exception import CustomException
from src.utils.feature_engineering import compute_ratio_columnwise
from src.utils.other_utils import read_yaml_file
import os,sys

# Load the configuration file
inference_config = read_yaml_file("src/config/inference_config.yaml")

selected_features=inference_config['selected_features']
categorical_features=inference_config['categorical_features']
threshold = inference_config['threshold']


def preprocessing(df:pd.DataFrame)->pd.DataFrame:
    """
    Preprocess the input data
    """
    # Drop rows with missing values
    df['AMT_CREDIT_AMT_GOODS_PRICE_ratio'] = compute_ratio_columnwise(df, 'AMT_CREDIT', 'AMT_GOODS_PRICE')
    df[categorical_features] = df[categorical_features].astype('category')
    df = df[selected_features]
    return df



def get_top_3_shap_features(shap_values: dict, prob: float, threshold: float=threshold,top_n=3) -> dict:
    """
    Selects the top 3 SHAP feature names based on probability and threshold.
    
    - If prob > threshold: Returns the 3 highest SHAP values (most positive).
    - If prob <= threshold: Returns the 3 lowest SHAP values (most negative).

    Args:
    shap_values (dict): Dictionary of feature SHAP values.
    prob (float): Predicted probability score.
    threshold (float): Threshold to compare probability.

    Returns:
    list: Top 3 selected feature names.
    """
    # Sort features by SHAP value in ascending order
    sorted_features = sorted(shap_values.items(), key=lambda x: x[1])  # Sort by value

    if prob > threshold:
        # Select top 3 features with highest SHAP values (most positive)
        top_3_features = dict(sorted_features[-top_n:])
    else:
        # Select bottom 3 features with lowest SHAP values (most negative)
        top_3_features = dict(sorted_features[:top_n])

    return top_3_features


