import json
import os
import sys
import argparse

def get_json_paths(main_path):
    """ Given a path to output/main, return a list of all relative paths to 
    every json file. 
    """
    pass

def write_two_plus_classfiers(json_paths):
    """ Given a list of all json paths, filter and write those nouns who have
    two or more classifiers for any homophone.
    """
    pass

def write_two_plus_homophones(json_paths):
    """ Given a list of all json paths, filter and write those nouns who have
    two or more homophones
    """
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-cl', action='store_true', help="write nouns with two or more classifiers")
    parser.add_argument('-ho', action='store_true', help="write nouns with two or more homophones")
    args = parser.parse_args()

    if not args.cl or not args.ho:
        parser.print_help()
        sys.exit()

    if args.cl or args.ho:
        json_paths = get_json_paths("./output/main/")
    
    if args.cl:
        write_two_plus_classfiers(json_paths)
    
    if args.ho:
        write_two_plus_homophones(json_paths)
    