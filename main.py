import argparse
import pandas as pd
import json
import os
import sys

import get_csvs as getter
import homophony_counter as counter

def get_syntax(syntax_type):
    """ Return the syntax specification 
    """
    syntax = ["cl n", "cl adv n", "cl adj n"]
    if syntax_type == "num_noun":
        syntax = ["num " + s for s in syntax]
    elif syntax_type == "dem_noun":
        syntax = ["dem " + s for s in syntax]
    elif syntax_type == "det_noun":
        syntax = ["det " + s for s in syntax]
    elif syntax_type == "not_noun":
        # POS_tags = ['pro:per', 'v:aux', 'conj', 'co', 'prep', 'n:relat', 'v:cop', 'pro:dem', 'v:resc', 'L2', 'pro:wh', 'v:dirc', 'n:fam', 'post', 'chi', 'v', 'adv', 'n:prop', 'poss', 'asp', 'det', 'adv:wh', 'adj', 'cl', 'num', 'n', 'on', 'cleft', 'sfp', 'nom', 'co:int']
        syntax = ["cl (?!(?:adj|adv))[^n][a-z:]*", "cl adv [^n][a-z:]*", "cl adj [^n][a-z:]*"]
    elif syntax_type == "all":
        syntax += ["cl (?!(?:adj|adv))[^n][a-z:]*", "cl adv [^n][a-z:]*", "cl adj [^n][a-z:]*"]
    return syntax

def handle_output_path(collection, language, want_children, syntax_type):
    """ Return output path, and create directories if they don't exist. 
    """
    corpora_type = "child" if want_children else "adult"

    if "output" not in os.listdir("./"):
        os.mkdir("./output")

    if "main" not in os.listdir("./output"):
        os.mkdir("./output/main")

    if corpora_type not in os.listdir("./output/main"):
        os.mkdir("./output/main/" + corpora_type)

    if syntax_type not in os.listdir("./output/main" + corpora_type):
        os.mkdir("./output/main/" + corpora_type + "/" + syntax_type)
    
    return "./output/{}/{}/{}_{}".format(corpora_type, syntax_type, collection, language)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--collection", help="collection name")
    parser.add_argument("-l", "--language", help="language name")
    parser.add_argument("-ch", "--want_children", help="y if child, n if adult")
    parser.add_argument("-s", "--syntax_type", help="syntax: all, noun, dem_noun, det_noun, num_noun, not_noun")
    args = parser.parse_args()
    
    if not args.collection or not args.language or not args.want_children or not args.syntax_type:
        parser.print_help()
        sys.exit()

    print("=== RUNNING CLASSIFIER ===")
    print("ARGUMENTS: {}, {}, {}, {}".format(args.collection, args.language, args.want_children, args.syntax_type))

    collection = args.collection
    language = args.language
    want_children = False if args.want_children == 'n' else True
    syntax_type = args.syntax_type

    getter.main(collection, language)

    syntax = get_syntax(syntax_type)
    data_cl, homophony_counter, unresolved = counter.main(collection, language, syntax, syntax_type, want_children)

    path = handle_output_path(collection, language, want_children, syntax_type)

    # print(unresolved)
    data_cl.to_csv(path + "_cl.csv")
    with open(path + ".json", 'w') as outfile:
        json.dump(homophony_counter, outfile, ensure_ascii=False, indent=4, sort_keys=True)
    with open(path + "_fail.txt", 'w') as outfile:
        unresolved = [item.to_string() for item in unresolved]
        outfile.write("\n\n".join(unresolved))