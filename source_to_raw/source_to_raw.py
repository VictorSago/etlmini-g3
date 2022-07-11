import os
import requests
import json, pprint


#CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

BASE_URL = "https://swapi.dev/api/"

def get_info(searchstring):
    '''a function that does a request to a URL and 
    returns the resource as a Python dict'''
    req_url = BASE_URL + searchstring
    resp = requests.get(req_url)
    if resp.status_code == 200:
        return json.loads(resp.text)
    return f"Fail! Response code: {resp.status_code}"

# def save_data2(dictionary, path):
#     '''A function that takes a Python dict and a filepath 
#     and saves the dict as a JSON object in that path'''
#     #print(os.getcwd())
#     file_path = path + "/data.json"
#     with open(file_path, "w") as f:
#         lines = []
#         lines.append("{")
#         for key, value in dictionary.items():
#             line = '"' + key + ': ' + str(value) + "\n"
#             lines.append()
#         lines.append("}")
#         f.writelines(lines)

def save_data(dictionary, path):
    '''A function that takes a Python dict and a filepath 
    and saves the dict as a JSON object in that path'''
    file_path = path + "/data.json"
    with open(file_path, "w") as f:
        json.dump(dictionary, f)

def source_to_file(searchstring):
    d = get_info(searchstring)
    save_data(d, "data/testing/raw")
