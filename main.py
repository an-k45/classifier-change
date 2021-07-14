import argparse
import pandas as pd
import json
import os

import get_csvs as getter
import homophony_counter as counter

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
    # TODO: Parse command line arguments
    collection = "Chinese"
    language = "Mandarin"
    want_children = False
    syntax_type = "noun_regular"

    syntax = ["cl n", "cl adv n", "cl adj n"]
    if syntax_type == "num":
        syntax = ["num " + s for s in syntax]
    elif syntax_type == "dem":
        syntax = ["dem " + s for s in syntax]
    elif syntax_type == "det":
        syntax = ["det " + s for s in syntax]
    # TODO: Admit syntax of the form cl v:pro (or other non-n endings), cl num, accounting for adv/adj in the middle. Use regex.

    getter.main(collection, language)

    data_cl, homophony_counter = counter.main(collection, language, syntax, want_children)

    path = handle_output_path(collection, language, want_children, syntax_type)

    data_cl.to_csv(path + "_cl.csv")
    with open(path + ".json", 'w') as outfile:
        json.dump(homophony_counter, outfile, ensure_ascii=False, indent=4, sort_keys=True)