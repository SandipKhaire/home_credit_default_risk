import sys
import os
from typing import Any, Dict, Optional
from src.logging.custom_logging import logger
from src.exceptions.custom_exception import CustomException
from pydantic import BaseModel,Field,field_validator


class PredictionRequest(BaseModel):
    EXT_SOURCE_3: Optional[float] = Field(
        ..., 
        description="Value must be between 0 and 1 and can be missing",
        json_schema_extra={"example": 0.617}
    )
    
    EXT_SOURCE_2: Optional[float] = Field(
        ..., 
        description="Value must be between 0 and 1 and can be missing",
        json_schema_extra={"example": 0.789}
    )
    
    EXT_SOURCE_1: Optional[float] = Field(
        ..., 
        description="Value must be between 0 and 1 and can be missing",
        json_schema_extra={"example": 0.123}
    )
    
    AMT_CREDIT: float = Field(
        ..., 
        description="Credit amount of the loan >0 and non-missing",
        json_schema_extra={"example": 100000}
    )
    
    AMT_ANNUITY: float = Field(
        ..., 
        description="Loan annuity",
        json_schema_extra={"example": 10000}
    )
    
    AMT_GOODS_PRICE: Optional[float] = Field(
        ..., 
        description="Goods price of the loan>0 and can be missing ",
        json_schema_extra={"example": 100000}
    )
    
    Client_Age: int = Field(
        ..., 
        description="Client's age in years between 20 and 100 and no missing",
        json_schema_extra={"example": 25}
    ) 
    
    employment_years: Optional[int] = Field(
        ..., 
        description="years since employed >=0 and can be missing",
        json_schema_extra={"example": 3}
    )
    
    NAME_EDUCATION_TYPE: str = Field(
        ..., 
        description="Education type of the client",
        json_schema_extra={"example": "Secondary / secondary special"}
    )
    
    ORGANIZATION_TYPE: str = Field(
        ..., 
        description="Organization type of the client",
        json_schema_extra={"example": "Business Entity Type 3"}
    )

    @field_validator('EXT_SOURCE_3','EXT_SOURCE_2','EXT_SOURCE_1')
    def check_ext_source(cls, v):
        if v is not None:
            if not(0<= v <=1) :
                raise ValueError('Value must be between 0 and 1 or None')
        return v
    
    @field_validator('AMT_CREDIT')
    def check_amt_credit(cls, v):
        if  not(v>0):
            raise ValueError('Value must be greater than 0 and Non-missing')
        return v
    
    @field_validator('AMT_GOODS_PRICE')
    def check_goods_price(cls, v):
        if v is not None and not(v>0):
            raise ValueError('Value must be greater than 0 and can be missing')
        return v
    
    @field_validator('Client_Age')
    def check_age(cls, v):
        if not(20<=v<=100) and not None:
            raise ValueError('Value must be between 20 and 100 and can not be missing')
        return v
    
    @field_validator('employment_years')
    def check_employment_years(cls, v):
        if v is not None and not(v>=0):
            raise ValueError('Value must be greater than or equal to 0 and can be missing')
        return v
    
    @field_validator('NAME_EDUCATION_TYPE')
    def check_education_type(cls, v):
        allowed_values = ['Secondary / secondary special', 
                          'Higher education', 'Incomplete higher', 
                          'Lower secondary', 'Academic degree']
        if v not in allowed_values :
            raise ValueError('Value must be one of Secondary / secondary special, Higher education, Incomplete higher, Lower secondary, Academic degree')
        return v
    
    @field_validator('ORGANIZATION_TYPE')
    def check_organization_type(cls, v):
        allowed_values = [
            'Self-employed', 'Agriculture', 'Business Entity Type 3', 'Construction', 
            'Industry: type 7', 'Medicine', 'XNA', 'School', 'Industry: type 4', 
            'Transport: type 2', 'Other', 'Kindergarten', 'Electricity', 'Government', 
            'Hotel', 'Industry: type 9', 'Business Entity Type 2', 'Industry: type 11', 
            'Business Entity Type 1', 'Realtor', 'Military', 'Housing', 'Industry: type 1', 
            'Services', 'Trade: type 7', 'Transport: type 4', 'Security Ministries', 
            'Trade: type 2', 'Trade: type 3', 'Security', 'Industry: type 3', 'Bank', 
            'Industry: type 2', 'Industry: type 12', 'Telecom', 'Police', 'Restaurant', 
            'Insurance', 'Postal', 'Trade: type 1', 'Emergency', 'Legal Services', 
            'Transport: type 1', 'Transport: type 3', 'University', 'Industry: type 5', 
            'Trade: type 6', 'Industry: type 10', 'Advertising', 'Trade: type 5', 'Mobile', 
            'Culture', 'Industry: type 13', 'Cleaning', 'Religion', 'Industry: type 6', 
            'Trade: type 4', 'Industry: type 8'
        ]
        if v not in allowed_values :
            raise ValueError('Value must be in given categories')
        return v
    


# Define response model
class PredictionResponse(BaseModel):
    request_id: str
    raw_feature_values: Dict[str, Any]
    model_features: Dict[str, Any]
    prediction_prob: Optional[float]=Field(...)
    status: str
    failure_reason: Dict[str, str] = {}
    top_3_reason_codes: Dict[str, float] = {}
    shap_values: Dict[str, float] = {}
    timestamp: str