import json
import os


##################################################################################################################
# Function Name: read_json
# Description  : Reads the given Json File.
# @param       : json_path (String) - Path where you would like to save json file
# @return      : Data Dictionary Object
##################################################################################################################
def read_json(json_path: str):
    with open(json_path) as f:
        data_dict = json.load(f)

    return data_dict
##################################################################################################################


##################################################################################################################
# Function Name: write_json
# Description  : Writes the given Json dictionary to a Json File
# @param       : json_data (Dictionary)
# @param       : json_path (String) - Path where you would like to save json file
##################################################################################################################
def write_json(json_data: dict, json_path: str):
    with open(json_path, 'w') as data_file:
        json.dump(json_data, data_file, indent=4)
##################################################################################################################


##################################################################################################################
# Function Name: search_file
# Description  : Traverses the directory and search the file
# @param       : Directory, which you would like to traverse
# @param       : File, which you would like to search
# @return      : List of the File Location(s)
##################################################################################################################
def search_file(directory: str, file_name: str) -> list:

    for dir_path, dir_names, files in os.walk(directory):
        for name in files:
            if file_name in name:
                return os.path.join(dir_path, name)
##################################################################################################################

