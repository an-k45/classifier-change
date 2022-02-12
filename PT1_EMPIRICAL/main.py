import argparse
import pandas as pd
import json
import os
import sys

# import get_csvs as getter
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-C", type=str, required=True, help="Collection name")
    parser.add_argument("-L", type=str, required=True, help="Language name")
    parser.add_argument("-T", type=str, required=True, help="Target group: child or adult")
    parser.add_argument("-S", type=str, required=True, help="Syntax type: all, noun, dem_noun, det_noun, num_noun, not_noun")

    args = parser.parse_args()

    print("=== RUNNING CLASSIFIER ===")
    print("ARGUMENTS: {}, {}, {}, {}".format(args.C, args.L, args.T, args.S))

    collection, language, syntax_type = args.C, args.L, args.S
    want_children = False if args.T == 'adult' else True

    # getter.main(collection, language)

    syntax = get_syntax(syntax_type)
    data_cl, homophony_counter, unresolved = counter.main(collection, language, syntax, syntax_type, want_children)

    out_dir = "./output/main/{}/{}/".format(args.T, syntax_type)
    os.makedirs(out_dir, exist_ok=True)
    out_path = out_dir + "{}_{}".format(collection, language)

    # print(unresolved)
    data_cl.to_csv(out_path + "_cl.csv")
    with open(out_path + ".json", 'w') as outfile:
        json.dump(homophony_counter, outfile, ensure_ascii=False, indent=4, sort_keys=True)
    with open(out_path + "_fail.txt", 'w') as outfile:
        unresolved = [item.to_string() for item in unresolved]
        outfile.write("\n\n".join(unresolved))