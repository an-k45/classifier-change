import argparse
import pandas as pd
import json
import os

import get_csvs as getter
import homophony_counter as counter

def get_syntax(syntax_type):
    """ Return the syntax specification 
    """
    syntax = ["cl n", "cl adv n", "cl adj n"]
    if syntax_type == "num":
        syntax = ["num " + s for s in syntax]
    elif syntax_type == "dem":
        syntax = ["dem " + s for s in syntax]
    elif syntax_type == "det":
        syntax = ["det " + s for s in syntax]
    elif syntax_type == "not_noun_all":
        # POS_tags = ['pro:per', 'v:aux', 'conj', 'co', 'prep', 'n:relat', 'v:cop', 'pro:dem', 'v:resc', 'L2', 'pro:wh', 'v:dirc', 'n:fam', 'post', 'chi', 'v', 'adv', 'n:prop', 'poss', 'asp', 'det', 'adv:wh', 'adj', 'cl', 'num', 'n', 'on', 'cleft', 'sfp', 'nom', 'co:int']
        syntax = ["cl (?!(?:adj|adv))[^n][a-z:]*", "cl adv [^n][a-z:]*", "cl adj [^n][a-z:]*"]
    return syntax

def handle_output_path(collection, language, want_children, syntax_type):
    """ Return output path, and create directories if they don't exist. 
    """
    corpora_type = "child" if want_children else "adult"

    if "output" not in os.listdir("./"):
        os.mkdir("./output")

    if corpora_type not in os.listdir("./output"):
        os.mkdir("./output/" + corpora_type)

    if syntax_type not in os.listdir("./output/" + corpora_type):
        os.mkdir("./output/" + corpora_type + "/" + syntax_type)
    
    return "./output/{}/{}/{}_{}".format(corpora_type, syntax_type, collection, language)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='collection', nargs='?', default='Chinese')
    parser.add_argument(dest='language', nargs='?', default='Mandarin')
    parser.add_argument(dest='want_children', nargs='?', default='no')
    parser.add_argument(dest='syntax_type', nargs='?', default='noun_all')
    args = parser.parse_args()

    collection = args.collection
    language = args.language
    want_children = False if args.want_children == 'no' else True
    syntax_type = args.syntax_type

    syntax = get_syntax(syntax_type)

    getter.main(collection, language)

    data_cl, homophony_counter, unresolved = counter.main(collection, language, syntax, want_children)

    path = handle_output_path(collection, language, want_children, syntax_type)

    # print(unresolved)
    data_cl.to_csv(path + "_cl.csv")
    with open(path + ".json", 'w') as outfile:
        json.dump(homophony_counter, outfile, ensure_ascii=False, indent=4, sort_keys=True)
    with open(path + "_fail.txt", 'w') as outfile:
        unresolved = [item.to_string() for item in unresolved]
        outfile.write("\n\n".join(unresolved))