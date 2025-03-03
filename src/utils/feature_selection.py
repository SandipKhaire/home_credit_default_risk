import pandas as pd
import numpy as np
import xgboost as xgb
import shap
from sklearn.model_selection import train_test_split



def shap_feature_selection(
    train_data: pd.DataFrame,
    target_name: str,
    feature_names: list = None,
    split_data: bool = True,
    test_size: float = 0.3,
    importance_threshold: float = 0.95,
    random_state: int = 42,
    model_params: dict = None,
    use_train_for_shap: bool = True,
    enable_categorical: bool = True,
    verbose: bool = False
):
    """
    Performs feature selection using SHAP values and XGBoost.
    
    Parameters:
    -----------
    train_data : pd.DataFrame
        DataFrame containing features and target variable
    target_name : str
        Name of the target column (required)
    feature_names : list, optional
        List of feature column names. If None, all columns except target will be used
    split_data : bool, default=True
        Whether to split data into train/test sets
    test_size : float, default=0.3
        Proportion of data to use for testing when split_data=True
    importance_threshold : float, default=0.95
        Cumulative importance threshold for feature selection
    random_state : int, default=42
        Random seed for reproducibility
    model_params : dict, optional
        Parameters for XGBoost model. If None, default parameters will be used
    use_train_for_shap : bool, default=True
        Whether to calculate SHAP values on training data (True) or test data (False)
    enable_categorical : bool, default=True
        Whether to enable XGBoost's native categorical feature support
    verbose : bool, default=False
        Whether to print progress information
    
    Returns:
    --------
    tuple
        (selected_features, shap_importance_df)
        - selected_features: List of selected feature names
        - shap_importance_df: DataFrame with feature importance information
    """
    # Validate that target_name exists in the dataframe
    if target_name not in train_data.columns:
        raise ValueError(f"Target column '{target_name}' not found in the provided DataFrame")
    
    # Handle feature names
    if feature_names is None:
        feature_names = [col for col in train_data.columns if col != target_name]
    
    # Extract features and target
    X = train_data[feature_names].copy()
    y = train_data[target_name].copy()
    
    # Default model parameters
    default_params = {
        'n_estimators': 100,
        'learning_rate': 0.05,
        'max_depth': 4,
        'random_state': random_state,
        'eval_metric': 'aucpr',
        'early_stopping_rounds': 20,
        'enable_categorical': enable_categorical
    }
    
    # Update with user-provided parameters if available
    if model_params is not None:
        default_params.update(model_params)
    
    # Calculate class balance for imbalanced datasets
    if len(y.unique()) == 2 and 'scale_pos_weight' not in default_params:
        scale_pos_weight = sum(y == 0) / max(sum(y == 1), 1)  # Avoid division by zero
        default_params['scale_pos_weight'] = scale_pos_weight
        if verbose:
            print(f"scale_pos_weight: {scale_pos_weight:.4f}")
    
    # Split data if requested
    if split_data:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y if len(y.unique()) < 10 else None
        )
        eval_set = [(X_test, y_test)]
    else:
        X_train, y_train = X, y
        eval_set = None
    
    # Initialize and train XGBoost model
    model = xgb.XGBClassifier(**default_params)
    
    # If enable_categorical is True, identify categorical columns
    if default_params.get('enable_categorical', False):
        categorical_columns = X_train.select_dtypes(include=['category', 'object']).columns.tolist()
        if categorical_columns and verbose:
            print(f"Detected {len(categorical_columns)} categorical features: {categorical_columns}")
        
        # Ensure categorical columns are properly typed
        for col in categorical_columns:
            X_train[col] = X_train[col].astype('category')
            if split_data:
                X_test[col] = X_test[col].astype('category')
    
    if eval_set is not None:
        model.fit(X_train, y_train, eval_set=eval_set, verbose=verbose)
    else:
        model.fit(X_train, y_train, verbose=verbose)
    
    # Use TreeExplainer for faster computation with tree-based models
    explainer = shap.TreeExplainer(model)
    
    # Calculate SHAP values on either training or test data
    if use_train_for_shap:
        if verbose:
            print("Calculating SHAP values on training data...")
        shap_values = explainer.shap_values(X_train)
    else:
        if split_data:
            if verbose:
                print("Calculating SHAP values on test data...")
            shap_values = explainer.shap_values(X_test)
        else:
            if verbose:
                print("Warning: use_train_for_shap=False but split_data=False, using training data for SHAP values")
            shap_values = explainer.shap_values(X_train)
    
    # For multi-class, take the mean absolute value across all classes
    if isinstance(shap_values, list):
        # For multi-class models, shap_values is a list of arrays, one per class
        mean_abs_shap_values = np.mean([np.abs(sv).mean(axis=0) for sv in shap_values], axis=0)
    else:
        # For binary classification, shap_values is a single array
        mean_abs_shap_values = np.abs(shap_values).mean(axis=0)
    
    # Create feature importance DataFrame
    shap_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'SHAP_Importance': mean_abs_shap_values
    })
    
    # Sort features by importance
    shap_importance_df = shap_importance_df.sort_values(by='SHAP_Importance', ascending=False)
    
    # Calculate relative and cumulative importance
    total_importance = shap_importance_df['SHAP_Importance'].sum()
    shap_importance_df['Relative_Importance'] = shap_importance_df['SHAP_Importance'] / total_importance
    shap_importance_df['Cumulative_Importance'] = shap_importance_df['Relative_Importance'].cumsum()
    
    # Select features based on cumulative importance threshold
    selected_features = shap_importance_df[
        shap_importance_df['Cumulative_Importance'] <= importance_threshold
    ]['Feature'].tolist()
    
    # Add the next feature to cross the threshold to ensure we meet or exceed the threshold
    if len(selected_features) < len(feature_names) and importance_threshold < 1.0:
        next_feature = shap_importance_df.iloc[len(selected_features)]['Feature']
        selected_features.append(next_feature)
    
    if verbose:
        print(f"Selected {len(selected_features)} features out of {len(feature_names)} "
              f"that explain at least {importance_threshold*100:.1f}% of model predictions")
    
    return selected_features, shap_importance_df