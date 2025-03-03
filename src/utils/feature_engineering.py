import numpy as np
import pandas as pd

def compute_ratio_columnwise(df, feature1, feature2):
    """
    Efficiently compute the ratio of two numerical columns with handling for missing values and zero division.

    Handling rules:
    - If feature1 is NaN → assign -1
    - If feature2 is NaN → assign -2
    - If both feature1 & feature2 are NaN → assign -3
    - If feature2 is 0 → assign -4
    - Otherwise, compute feature1 / feature2

    Parameters:
    - df: Pandas DataFrame
    - feature1: str, Name of the numerator column
    - feature2: str, Name of the denominator column

    Returns:
    - Pandas Series containing the computed ratio
    """
    # Initialize the result array with NaN
    result = np.full(df.shape[0], np.nan)

    # Define masks for different conditions
    is_feature1_nan = df[feature1].isna()
    is_feature2_nan = df[feature2].isna()
    is_feature2_zero = df[feature2] == 0

    # Apply handling rules
    result[is_feature1_nan & is_feature2_nan] = -3  # Both NaN
    result[is_feature1_nan & ~is_feature2_nan] = -1  # Only feature1 NaN
    result[~is_feature1_nan & is_feature2_nan] = -2  # Only feature2 NaN
    result[~is_feature1_nan & is_feature2_zero] = -4  # feature2 is zero

    # Compute the ratio where valid
    valid_ratio_mask = ~(is_feature1_nan | is_feature2_nan | is_feature2_zero)
    result[valid_ratio_mask] = (df.loc[valid_ratio_mask, feature1] / df.loc[valid_ratio_mask, feature2]).round(2)

    return pd.Series(result, index=df.index)  # Return as Pandas Series