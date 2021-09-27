import json
import os
import sys
import argparse

def get_json_paths(main_path):
    """ Given a path to output/main, return a list of all relative paths to 
    every json file. 
    """
    json_paths = []
    for entry in os.listdir(main_path):
        cur_path = os.path.join(main_path, entry)
        if not os.path.isfile(cur_path):
            for dir in os.listdir(cur_path):
                sub_path = os.path.join(cur_path, dir)
                for file in os.listdir(sub_path):
                    if file.endswith(".json"):
                        json_paths.append(os.path.join(sub_path, file))
    
    return json_paths

def get_output_path(path, target):
    """ Given the path to a JSON file from main, swap main for the inputted target
    """
    parts = path.split('/')
    parts[2] = target
    
    cur_path = "."
    for dir in parts[1:-1]:
        next_path = os.path.join(cur_path, dir)
        if dir not in os.listdir(cur_path):
            os.mkdir(next_path)
        cur_path = next_path

    return '/'.join(parts)

def get_two_plus_classifiers(data):
    """ Given an JSON object with the phone-symbol-classifier frequency
    relationships, filter it for only those entries with two or more classifiers.
    """
    filtered_data = {}
    for phone in data.keys():
        for symbol in data[phone].keys():
            if len(data[phone][symbol].keys()) >= 2:
                if phone not in filtered_data:
                    filtered_data[phone] = {}
                if symbol not in filtered_data[phone]:
                    filtered_data[phone][symbol] = data[phone][symbol]
    return filtered_data

def write_two_plus_classfiers(json_paths):
    """ Given a list of all json paths, filter and write those nouns who have
    two or more classifiers for any homophone.
    """
    for path in json_paths:
        with open(path, "r") as in_f:
            data = json.load(in_f)
        filtered_data = get_two_plus_classifiers(data)
        output_path = get_output_path(path, 'cl_two_plus')
        with open(output_path, 'w') as out_f:
            json.dump(filtered_data, out_f, ensure_ascii=False, indent=4, sort_keys=True)

def get_two_plus_homophones(data):
    """ Given an JSON object with the phone-symbol-classifier frequency
    relationships, filter it for nouns with two or more homophones.
    """
    filtered_data = {}
    for phone in data.keys():
        if len(data[phone].keys()) >= 2:
            if phone not in filtered_data:
                filtered_data[phone] = data[phone]
    return filtered_data

def write_two_plus_homophones(json_paths):
    """ Given a list of all json paths, filter and write those nouns who have
    two or more homophones
    """
    for path in json_paths:
        with open(path, "r") as in_f:
            data = json.load(in_f)
        filtered_data = get_two_plus_homophones(data)
        output_path = get_output_path(path, 'hom_two_plus')
        with open(output_path, 'w') as out_f:
            json.dump(filtered_data, out_f, ensure_ascii=False, indent=4, sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-cl', action='store_true', help="write nouns with two or more classifiers")
    parser.add_argument('-hom', action='store_true', help="write nouns with two or more homophones")
    args = parser.parse_args()

    if not args.cl or not args.hom:
        parser.print_help()
        sys.exit()

    if args.cl or args.hom:
        json_paths = get_json_paths("./output/main")
        # print(json_paths)
    
    if args.cl:
        write_two_plus_classfiers(json_paths)
    
    if args.hom:
        write_two_plus_homophones(json_paths)
    