# tests/test_models.py
import pytest
from pydantic import ValidationError
from src.inference.request_validation import PredictionRequest

# Example valid data fixture - reusable in multiple tests
@pytest.fixture
def valid_prediction_data():
    return {
        "EXT_SOURCE_3": 0.617,
        "EXT_SOURCE_2": 0.789,
        "EXT_SOURCE_1": 0.123,
        "AMT_CREDIT": 100000,
        "AMT_ANNUITY": 10000,
        "AMT_GOODS_PRICE": 100000,
        "Client_Age": 25,
        "employment_years": 3,
        "NAME_EDUCATION_TYPE": "Secondary / secondary special",
        "ORGANIZATION_TYPE": "Business Entity Type 3"
    }

def test_valid_prediction_request(valid_prediction_data):
    """Test that valid data passes validation."""
    # This should not raise an exception
    request_obj = PredictionRequest(**valid_prediction_data)
    # We can also assert specific properties if needed
    assert request_obj.EXT_SOURCE_3 == 0.617
    assert request_obj.Client_Age == 25

def test_invalid_ext_source(valid_prediction_data):
    """Test validation with invalid EXT_SOURCE values."""
    invalid_data = valid_prediction_data.copy()
    invalid_data["EXT_SOURCE_3"] = 1.5  # Out of range
    
    with pytest.raises(ValidationError) as exc_info:
        PredictionRequest(**invalid_data)
    
    # We can also assert details about the validation error
    error_details = str(exc_info.value)
    assert "EXT_SOURCE_3" in error_details
    assert "value must be between 0 and 1" in error_details.lower() 

def test_invalid_credit_amount(valid_prediction_data):
    """Test validation with invalid AMT_CREDIT."""
    invalid_data = valid_prediction_data.copy()
    invalid_data["AMT_CREDIT"] = -1000  # Negative value
    
    with pytest.raises(ValidationError):
        PredictionRequest(**invalid_data)


# You can add more test cases using pytest's parameterize feature
@pytest.mark.parametrize("field,invalid_value,expected_error", [
    ("EXT_SOURCE_1", 2.0, "value must be between 0 and 1"),
    ("EXT_SOURCE_1", -0.5, "value must be between 0 and 1"),
    ("Client_Age", 120, "value must be between 20 and 100"),
    ("employment_years", -1, "greater than or equal")
])
def test_multiple_invalid_fields(valid_prediction_data, field, invalid_value, expected_error):
    """Test multiple invalid field values with parameterization."""
    invalid_data = valid_prediction_data.copy()
    invalid_data[field] = invalid_value
    
    with pytest.raises(ValidationError) as exc_info:
        PredictionRequest(**invalid_data)
    
    assert expected_error in str(exc_info.value).lower()
