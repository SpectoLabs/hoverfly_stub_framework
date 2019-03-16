from .hoverfly_helpers import *


# Replace Plan Code with regex
def make_plan_code_global():
    update_path_matcher_value_together_for_all_apis('regex', "/C[DQ]/", "/C[DQ]/")
    print("CUSTOM INFO: Updated Plan Code for all requests...")


# Replace Member/Transaction Ids with regex
def make_member_and_transaction_id_global():
    update_path_matcher_value_together_for_all_apis('regex', "/[0-9]*/", "/[0-9]+/")
    update_path_matcher_value_together_for_all_apis('regex', "[0-9]+$", "[0-9]+$")
    print("CUSTOM INFO: Updated Member/Transaction Id for all requests...")


# Replace all the query parameters with global *
def make_query_parameters_global():
    update_query_matcher_values_for_all_apis()
    print("CUSTOM INFO: Updated Query Matcher and Values for all requests...")


# Remove Request Body for all APIs
def remove_request_body_for_all_requests():
    remove_node_from_all_apis('request', 'body')
    print("CUSTOM INFO: Removed Request Body for all requests...")


# Remove Body for all APIs
def remove_request_query_for_all_requests():
    remove_node_from_all_apis('request', 'query')
    print("CUSTOM INFO: Removed Query Params for all requests...")


# Create Stub API Collection
def create_final_stub_api_collection():
    create_stub_api_collection_and_response_data()
    print("CUSTOM INFO: Updated default_stub_api_responses and API_Collection_and_Latency.csv...")


# Update Responses of the APIs
def update_response_of_required_apis():

    # Update Response Body for API: POST - super/api/member/v1/plans/*/members/*/rollover
    update_stub_api_response_status_and_body("API_2", 201, False)
    update_stub_config_headers('API_2', 'response', 'Content-Type', 'application/json; charset=utf-8')
    remove_stub_config_headers('API_2', 'response', 'Content-Encoding')
    print('CUSTOM INFO: Updated Response for API: '
          'POST - API_2')
