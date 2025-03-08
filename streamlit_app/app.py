import streamlit as st
import requests
import json

# FastAPI endpoint
API_URL = "http://localhost:8000/predict"  # Change to your deployed API URL if hosted remotely

st.title("Credit Risk Prediction")

# User Inputs with Constraints
st.sidebar.header("Input Features")

# Function to create optional sliders
def optional_slider(label, min_val, max_val, default_val):
    allow_none = st.sidebar.checkbox(f"Allow None for {label}")
    return None if allow_none else st.sidebar.slider(label, min_val, max_val, default_val)

EXT_SOURCE_3 = optional_slider("EXT_SOURCE_3 (0 to 1)", 0.0, 1.0, 0.617)
EXT_SOURCE_2 = optional_slider("EXT_SOURCE_2 (0 to 1)", 0.0, 1.0, 0.789)
EXT_SOURCE_1 = optional_slider("EXT_SOURCE_1 (0 to 1)", 0.0, 1.0, 0.123)
AMT_CREDIT = st.sidebar.number_input("Credit Amount (AMT_CREDIT) > 0", min_value=1, value=100000)
AMT_ANNUITY = st.sidebar.number_input("Loan Annuity (AMT_ANNUITY)", min_value=1, value=10000)
AMT_GOODS_PRICE = st.sidebar.number_input("Goods Price (AMT_GOODS_PRICE) > 0", min_value=1, value=100000)
Client_Age = st.sidebar.slider("Client Age (20 to 100)", 20, 100, 25)
employment_years = st.sidebar.slider("Years of Employment (>=0)", 0, 50, 3)

NAME_EDUCATION_TYPE = st.sidebar.selectbox(
    "Education Type",
    ['Secondary / secondary special', 
                          'Higher education', 'Incomplete higher', 
                          'Lower secondary', 'Academic degree']
)

ORGANIZATION_TYPE = st.sidebar.selectbox(
    "Organization Type",
    [
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
)

# Create the request JSON
request_data = {
    "EXT_SOURCE_3": EXT_SOURCE_3 if EXT_SOURCE_3 is not None else None,
    "EXT_SOURCE_2": EXT_SOURCE_2,
    "EXT_SOURCE_1": EXT_SOURCE_1,
    "AMT_CREDIT": AMT_CREDIT,
    "AMT_ANNUITY": AMT_ANNUITY,
    "AMT_GOODS_PRICE": AMT_GOODS_PRICE,
    "Client_Age": Client_Age,
    "employment_years": employment_years,
    "NAME_EDUCATION_TYPE": NAME_EDUCATION_TYPE,
    "ORGANIZATION_TYPE": ORGANIZATION_TYPE
}

# Submit button
if st.sidebar.button("Predict"):
    st.subheader("Prediction Result")
    
    try:
        response = requests.post(API_URL, json=request_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            
            st.success(f"Prediction Probability: {result['prediction_prob']:.4f}")
            if result['prediction_prob'] > 0.49781528:
                st.markdown(
                    '<p style="color:red; font-size:18px; font-weight:bold;">🚨 Customer is Risky. Loan Not Approved.</p>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<p style="color:green; font-size:18px; font-weight:bold;">✅ Customer is Low Risk. Loan Approved!</p>',
                    unsafe_allow_html=True
                )

            st.write("Top 3 Reasons/Variables Influencing Prediction:")
            st.json(result["top_3_reason_codes"])


        else:
            st.error(f"API Request Failed! Error: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Error: {str(e)}")
