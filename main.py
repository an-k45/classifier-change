import argparse
import pandas as pd
import json

import get_csvs as getter
import homophony_counter as counter

if __name__ == "__main__":
    # TODO: Parse command line arguments
    collection = "Chinese"
    language = "Mandarin"
    syntax = ["cl n", "cl adv n"]

    getter.main(collection, language)

    homophony_counter = counter.main(collection, language, syntax)

    with open('output/{}_{}.json'.format(collection, language), 'w') as outfile:
        json.dump(homophony_counter, outfile, ensure_ascii=False, indent=4, sort_keys=True)