from .common_helpers import *
import global_variables as global_var
import re
import os.path
import pandas as pd
from shutil import copyfile
import datetime
import sys


##################################################################################################################
# Function Name: create_stub_api_collection_and_response_data
# Description  : Reads Stub Config json and creates API_Collection_and_Latency.csv and takes backup of the csv in
#                case there has been any change. Moreover, it also writes the individual responses of all the APIs
#                present in Stub Config to data --> default_stub_api_responses directory.
# Author       : Navdit Sharma
# Comments     : Created on 13/03/2019
##################################################################################################################
def create_stub_api_collection_and_response_data():

    # Make Regex Path Values more robust
    make_regex_values_more_robust()

    # Create Dataframe of csv
    api_collection_latency_df = pd.DataFrame(columns=['API_Identifier', 'Method', 'Path', 'Latency'])

    # Read Stub Config Json
    json_dict = read_json(global_var.stub_config_path)
    node_id = 0
    for node_dict in json_dict["data"]["pairs"]:
        path = json_dict["data"]["pairs"][node_id]["request"]["path"][0]["value"]
        api_method = json_dict["data"]["pairs"][node_id]["request"]["method"][0]["value"]
        api_response = json_dict["data"]["pairs"][node_id]["response"]["body"]
        api_identifier = "API_" + str(node_id+1)

        # Filling Dataframe
        api_collection_latency_df.loc[node_id] = [api_identifier, api_method, path, 0]

        # Saving Stub API Responses
        create_stub_api_response_json(api_identifier, api_response)

        node_id = node_id + 1

    # Save API Collection and Latency into csv
    # Create backup of existing API_Collection_and_Latency.csv
    if os.path.isfile(global_var.api_collection_latency_csv):
        # Compare old and new csv for any changes
        api_collection_latency_df_old = pd.read_csv(global_var.api_collection_latency_csv)

        # Check for changes in CSV
        if len(api_collection_latency_df_old.index) == len(api_collection_latency_df.index):
            if (api_collection_latency_df_old[['Method']].values == api_collection_latency_df[['Method']].values).all():
                if (api_collection_latency_df_old[['Path']].values == api_collection_latency_df[['Path']].values).all():
                    # This will make sure that Latency values are updated in sheet of hoverfly_stub during second run.
                    copyfile(global_var.api_collection_latency_csv, os.path.join(global_var.hoverfly_stub_folder,
                                                                                 "API_Collection_and_Latency.csv"))
        # If there is a difference in the new csv and old csv then take backup
        else:
            current_time = (datetime.datetime.now()).strftime("%H%M%S")
            dest_path = os.path.join(global_var.backup_folder + "/API_Collection_and_Latency_" + current_time + ".csv")
            # Take Backup
            copyfile(global_var.api_collection_latency_csv, dest_path)

            # Create csv
            api_collection_latency_df.to_csv(global_var.api_collection_latency_csv, sep=',', index=False)
            # Copy to hoverfly_stub folder
            copyfile(global_var.api_collection_latency_csv, os.path.join(global_var.hoverfly_stub_folder,
                                                                         "API_Collection_and_Latency.csv"))
            print("CUSTOM INFO: Please update Latency Column in csv, as file has been changed")

    # No back up needs to be done.
    else:
        api_collection_latency_df.to_csv(global_var.api_collection_latency_csv, sep=',', index=False)
        # Copy to hoverfly_stub folder
        copyfile(global_var.api_collection_latency_csv, os.path.join(global_var.hoverfly_stub_folder,
                                                                     "API_Collection_and_Latency.csv"))
##################################################################################################################


##################################################################################################################
# Function Name: create_stub_api_response_json
# Description  : Creates a json file for the given API Name and Response Body.
# @param       : api_identifier (string) - unique name of the API.
# @param       : api_response_body (string) - response body, which needs to be written to Json file
# Author       : Navdit Sharma
# Comments     : Created on 13/03/2019
##################################################################################################################
def create_stub_api_response_json(api_identifier: str, api_response_body: str):
    try:
        response_data = json.loads(api_response_body)

        # Write response to stub_api_response folder
        api_response_path = os.path.join(global_var.api_default_responses_dir, "{}.json".format(api_identifier))
        write_json(response_data, api_response_path)
    except ValueError:
        api_response_path = os.path.join(global_var.api_default_responses_dir, "{}.txt".format(api_identifier))
        with open(api_response_path, 'w') as response_file:
            response_file.write(api_response_body)
##################################################################################################################


##################################################################################################################
# Function Name: search_node_id
# Description  : Retrieves the node id of the given api (path) from the given data dictionary.
# @param       : json_data (dict) - json in format of data dictionary
# @param       : api_path (string) - API Path, which needs to be looked for in the given data.
# @param       : api_method (string) - API Method of the given API Path.
# @return      : node_id (int), which can be used to correctly identify request in Stub Config.
# Author       : Navdit Sharma
# Comments     : Created on 06/03/2019
##################################################################################################################
def search_node_id(json_data: dict, api_path: str, api_method: str):
    node_id = 0

    for node_dict in json_data["data"]["pairs"]:
        path = json_data["data"]["pairs"][node_id]["request"]["path"][0]["value"]
        method = json_data["data"]["pairs"][node_id]["request"]["method"][0]["value"]
        if path == api_path and method == api_method:
            flag = True
            return node_id
        node_id = node_id + 1
##################################################################################################################


##################################################################################################################
# Function Name: delete_particular_node
# Description  : Delete Element from Stub Config Jason "Request" or "Response" Node
# @param       : api_identifier (str) - Unique API Name
# @param       : http_msg_type (string) - Request or Response
# @param       : node_name (string) - Can be body, query etc.
# Author       : Navdit Sharma
# Comments     : Created on 07/03/2019
##################################################################################################################
def delete_particular_node(api_identifier: str, http_msg_type: str, node_name: str):
    # Search API in Stub Config
    node_index = check_stub_api_collection_and_return_node_id(api_identifier)
    stub_json_data = read_json(global_var.stub_config_path)

    # Remove the given header
    if node_index is not None:
        if node_name in stub_json_data["data"]["pairs"][node_index][http_msg_type]:
            del stub_json_data["data"]["pairs"][node_index][http_msg_type][node_name]

        # Save it back to Stub Config
        write_json(stub_json_data, global_var.stub_config_path)
    else:
        print("CUSTOM ERROR: Node - Index was not found for API {} in delete_element_json".format(api_identifier))
##################################################################################################################


##################################################################################################################
# Function Name: remove_node_from_all_apis
# Description  : Removes given node (eg body, query etc) from all the APIs request in the Stub Config.
# @param       : http_msg_type (string) - Request or Response
# @param       : node_name (string) - Can be body, query etc.
# Author       : Navdit Sharma
# Comments     : Created on 07/03/2019
##################################################################################################################
def remove_node_from_all_apis(http_msg_type: str, node_name: str):
    # Read Stub Config Json
    stub_json_data = read_json(global_var.stub_config_path)

    # Delete Node
    node_id = 0
    for node_dict in stub_json_data["data"]["pairs"]:
        if node_name in stub_json_data["data"]["pairs"][node_id][http_msg_type]:
            del stub_json_data["data"]["pairs"][node_id][http_msg_type][node_name]

        node_id = node_id + 1

    # Save it back to Stub Config
    write_json(stub_json_data, global_var.stub_config_path)
##################################################################################################################


##################################################################################################################
# Function Name: update_request_path_matcher
# Description  : Updates the path matcher value of the APIs.
# @param       : api_path (string) - Path of the API
# @param       : api_method (string) - Method of the API
# @param       : matcher_type (string) - Values can be exact, glob, regex, xml, xpath, json, jsonpath
# Author       : Navdit Sharma
# Comments     : Created on 08/03/2019
##################################################################################################################
def update_request_path_matcher(api_path: str, api_method: str, matcher_type: str):
    # Read Stub Config
    json_dict = read_json(global_var.stub_config_path)

    # Search for the api path in Stub Config
    node_index = search_node_id(json_dict, api_path, api_method)

    # Update Request -> Path -> Matcher
    json_dict["data"]["pairs"][node_index]["request"]["path"][0]["matcher"] = matcher_type

    # Save Jason back
    write_json(json_dict, global_var.stub_config_path)
##################################################################################################################


##################################################################################################################
# Function Name: make_regex_values_more_robust
# Description  : Appends $ at the end of the Values, so as to make matching more robust and unique for Hoverfly.
# Author       : Navdit Sharma
# Comments     : Created on 16/03/2019
##################################################################################################################
def make_regex_values_more_robust():
    # Read Stub Config
    stub_json_data = read_json(global_var.stub_config_path)

    node_id = 0
    for node_dict in stub_json_data["data"]["pairs"]:
        # Check for all Child Nodes of Request Node
        for child_node in stub_json_data["data"]["pairs"][node_id]["request"]:
            if stub_json_data["data"]["pairs"][node_id]["request"][child_node][0]['matcher'] == 'regex':
                matcher_value = stub_json_data["data"]["pairs"][node_id]["request"][child_node][0]['value']
                if not str(matcher_value).endswith("$"):
                    final_matcher_value = str(matcher_value) + '$'
                    stub_json_data["data"]["pairs"][node_id]["request"][child_node][0]['value'] = final_matcher_value

        # Increment Nodes to traverse through all the requests
        node_id = node_id + 1

    # Save Jason back
    write_json(stub_json_data, global_var.stub_config_path)
##################################################################################################################


##################################################################################################################
# Function Name: update_request_path_matcher
# Description  : Updates the path matcher value of the APIs.
# @param       : api_path (string) - Path of the API
# @param       : api_method (string) - Method of the API
# @param       : matcher_type (string) - Values can be exact, glob, regex, xml, xpath, json, jsonpath
# Author       : Navdit Sharma
# Comments     : Created on 08/03/2019
##################################################################################################################
def update_request_path_value(api_path: str, api_method: str, find_value_substring: str, replace_value_substring: str,
                              is_find_value_substring_regex: bool):
    # Read Stub Config
    json_dict = read_json(global_var.stub_config_path)

    # Search for the api path in Stub Config
    node_index = search_node_id(json_dict, api_path, api_method)

    # Update Request -> Path -> Value
    path = json_dict["data"]["pairs"][node_index]["request"]["path"][0]["value"]

    if is_find_value_substring_regex:
        new_path = re.sub(find_value_substring, replace_value_substring, path)
    else:
        new_path = path.replace(find_value_substring, replace_value_substring)

    # Update Stub Config with new path
    json_dict["data"]["pairs"][node_index]["request"]["path"][0]["value"] = new_path

    # Save Jason back
    write_json(json_dict, global_var.stub_config_path)
##################################################################################################################


##################################################################################################################
# Function Name: update_path_matcher_value_together_for_all_apis
# Description  : Updates the path value as well as its matcher value of all the APIs.
# @param       : matcher (string) - Values can be exact, glob, regex, xml, xpath, json, jsonpath
# @param       : regex_str (string) - Regex expression to search the path for a value
# @param       : replace_path_value (string) - Once the value is found replace with this value.
# Author       : Navdit Sharma
# Comments     : Created on 08/03/2019
##################################################################################################################
def update_path_matcher_value_together_for_all_apis(matcher: str, regex_str: str, replace_path_value: str):
    # Read Stub Config Json
    json_dict = read_json(global_var.stub_config_path)

    # Compiling regex
    regex = re.compile(regex_str)

    # Replace /CD/ with /*/ and matcher value as glob
    node_id = 0
    for node_dict in json_dict["data"]["pairs"]:
        path = json_dict["data"]["pairs"][node_id]["request"]["path"][0]["value"]
        api_method = json_dict["data"]["pairs"][node_id]["request"]["method"][0]["value"]

        if regex.search(path):
            update_request_path_matcher(path, api_method, matcher)
            update_request_path_value(path, api_method, regex_str, replace_path_value, True)

        node_id = node_id + 1
##################################################################################################################


##################################################################################################################
# Function Name: update_query_matcher_values_for_all_apis
# Description  : Changes the Query matcher to 'glob' and value to * in all APIs of the stub config.
# Author       : Navdit Sharma
# Comments     : Created on 08/03/2019
##################################################################################################################
def update_query_matcher_values_for_all_apis():
    # Read Json
    json_dict = read_json(global_var.stub_config_path)

    node_id = 0
    for node_dict in json_dict["data"]["pairs"]:
        if "query" in json_dict["data"]["pairs"][node_id]["request"]:
            query_dict = json_dict["data"]["pairs"][node_id]["request"]["query"]

            if bool(query_dict):
                for key in list(query_dict):
                    query_dict[key][0]['matcher'] = 'glob'
                    query_dict[key][0]['value'] = '*'

        node_id = node_id + 1

    # Save Jason back
    write_json(json_dict, global_var.stub_config_path)
##################################################################################################################


##################################################################################################################
# Function Name: check_stub_api_collection_and_return_node_id
# Description  : Reads the API_Collection_and_Latency.csv and get the node id of the given API Identifier in the
#                Stub Config.
# @param       : api_identifier (string) - Unique name of API as given in API_Collection_and_Latency.csv
# @return      : Returns the node id (int) index in the Stub Config Json
# Author       : Navdit Sharma
# Comments     : Created on 07/03/2019
##################################################################################################################
def check_stub_api_collection_and_return_node_id(api_identifier: str):
    # Check if API_Collection_and_Latency.csv exists
    if not os.path.isfile(global_var.api_collection_latency_csv):
        create_stub_api_collection_and_response_data()

    # Read API Collection CSV
    api_collection_df = pd.read_csv(global_var.api_collection_latency_csv)
    if (api_collection_df[api_collection_df['API_Identifier'].isin([api_identifier])]).empty:
        print("CUSTOM ERROR: {} not found in API_Collection_and_Latency.csv".format(api_identifier))
        sys.exit(1)
    else:
        api_path = api_collection_df.loc[api_collection_df['API_Identifier'] == api_identifier, 'Path'].iloc[0]
        api_method = api_collection_df.loc[api_collection_df['API_Identifier'] == api_identifier, 'Method'].iloc[0]

        # Search API in Stub Config
        stub_json_data = read_json(global_var.stub_config_path)
        node_index = search_node_id(stub_json_data, api_path, api_method)

        return node_index
##################################################################################################################


##################################################################################################################
# Function Name: update_stub_api_response_status_and_body
# Description  : Checks the folder (data --> updated_stub_api_responses) to pick up the new response of the given
#                API and update it in Stub Config with given Status Code and Updated Response
#                Stub Config.
# @param       : api_identifier (string) - Unique name of API as given in API_Collection_and_Latency.csv
# @param       : status_code (int) - It can be any valid HTTP Status Code
# @param       : set_encoding (bool) - update the 'encodedBody' boolean value.
# Author       : Navdit Sharma
# Comments     : Created on 07/03/2019
##################################################################################################################
def update_stub_api_response_status_and_body(api_identifier: str, status_code: int, set_encoding: bool):
    # Search for the response file
    new_api_response_path = search_file(global_var.api_updated_responses_dir, api_identifier)

    # Error Handling in case Updated Stub API Responses Dir is incorrect
    if new_api_response_path is None:
        print("CUSTOM ERROR: Please check API Updated Response Exists for API Identifier {} in directory- {}".
              format(api_identifier, global_var.api_updated_responses_dir))

    # Search API in Stub Config
    node_index = check_stub_api_collection_and_return_node_id(api_identifier)
    if node_index is None:
        print("CUSTOM ERROR: Possible bug. Please follow steps:"
              "1. Check if the API Identifier given to the function exists in CSV"
              "2. If it exists, please delete the csv kept in data folder and hoverfly stub folder"
              "3. After deletion of csv please run main.py again.")
    stub_json_data = read_json(global_var.stub_config_path)

    # Update Response Status Code
    stub_json_data["data"]["pairs"][node_index]["response"]["status"] = status_code

    # Remove Encoding
    stub_json_data["data"]["pairs"][node_index]["response"]["encodedBody"] = set_encoding

    if 'json' in new_api_response_path:
        read_updated_json_response = read_json(new_api_response_path)

        # Update Response Body
        stub_json_data["data"]["pairs"][node_index]["response"]["body"] = json.dumps(read_updated_json_response)

    else:
        with open(new_api_response_path, 'r') as response_file:
            response_str = response_file.read()

        # Update Response Body
        stub_json_data["data"]["pairs"][node_index]["response"]["body"] = response_str

    # Save Jason back
    write_json(stub_json_data, global_var.stub_config_path)
##################################################################################################################


##################################################################################################################
# Function Name: update_stub_config_headers
# Description  : Updates the header of the "request" or "response" in the stub config json.
#                Stub Config.
# @param       : api_identifier (string) - Unique name of API as given in API_Collection_and_Latency.csv
# @param       : http_msg_type (str) - Can be 'request' or 'response'
# @param       : header_name (str) - Valid HTTP Header name
# @param       : header_value (str) - Valid HTTP Header value
# Author       : Navdit Sharma
# Comments     : Created on 07/03/2019
##################################################################################################################
def update_stub_config_headers(api_identifier: str, http_msg_type: str, header_name: str, header_value: str):
    # Search API in Stub Config
    node_index = check_stub_api_collection_and_return_node_id(api_identifier)
    stub_json_data = read_json(global_var.stub_config_path)

    # Update Header
    stub_json_data["data"]["pairs"][node_index][http_msg_type]["headers"][header_name] = [header_value]

    # Save it back to Stub Config
    write_json(stub_json_data, global_var.stub_config_path)
##################################################################################################################


##################################################################################################################
# Function Name: remove_stub_config_headers
# Description  : Removes the given header of the "request" or "response" in the stub config json.
#                Stub Config.
# @param       : api_identifier (string) - Unique name of API as given in API_Collection_and_Latency.csv
# @param       : http_msg_type (str) - Can be 'request' or 'response'
# @param       : header_name (str) - Valid HTTP Header name
# Author       : Navdit Sharma
# Comments     : Created on 07/03/2019
##################################################################################################################
def remove_stub_config_headers(api_identifier: str, http_msg_type: str, header_name: str):
    # Search API in Stub Config
    node_index = check_stub_api_collection_and_return_node_id(api_identifier)
    stub_json_data = read_json(global_var.stub_config_path)

    # Remove the given header
    if node_index is not None:
        if header_name in stub_json_data["data"]["pairs"][node_index][http_msg_type]['headers']:
            del stub_json_data["data"]["pairs"][node_index][http_msg_type]['headers'][header_name]

        # Save it back to Stub Config
        write_json(stub_json_data, global_var.stub_config_path)
    else:
        print("CUSTOM ERROR: Node Index was not found for API {} in remove_stub_config_headers".format(api_identifier))
##################################################################################################################
