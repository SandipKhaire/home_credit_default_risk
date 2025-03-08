import time
import requests
import json
import concurrent.futures

# API endpoint URL
API_URL = "http://localhost:8000/predict"

# Sample request data
request_data = {
    "EXT_SOURCE_3": 0.643026,
    "EXT_SOURCE_2": 0.90,
    "EXT_SOURCE_1": 0.675243,
    "AMT_CREDIT": 135801.6,
    "AMT_ANNUITY": 12345,
    "AMT_GOODS_PRICE": 123456,
    "Client_Age": 20,
    "employment_years": 3,
    "NAME_EDUCATION_TYPE": "Higher education",
    "ORGANIZATION_TYPE": "Self-employed",
}

def make_single_request(request_id=None):
    """Make a single request to the API and print the response"""
    print(f"Sending request {request_id} to Credit Risk API...")
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json=request_data, timeout=10)
        end_time = time.time()
        response_time = end_time - start_time

        print(f"Request {request_id} | Response Time: {response_time:.2f} seconds")

        if response.status_code == 200:
            print(f"Request {request_id} | API Request Successful!")
            result = response.json()
            print(json.dumps(result, indent=2))
        else:
            print(f"Request {request_id} | API Request Failed! Status Code: {response.status_code}")
            print(f"Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"Request {request_id} | Error: Could not connect to the API.")
    except requests.exceptions.Timeout:
        print(f"Request {request_id} | Error: Request timed out.")
    except Exception as e:
        print(f"Request {request_id} | Error: {str(e)}")

if __name__ == "__main__":
    #num_requests = 5  # Number of concurrent requests

    #with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
    #    futures = [executor.submit(make_single_request, i) for i in range(num_requests)]
        
    #    for future in concurrent.futures.as_completed(futures):
    #        future.result()  # Wait for all requests to complete
    
    make_single_request()
