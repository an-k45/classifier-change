import childespy as cpy
import pandas as pd 
import os

COLLECTIONS = {
    "Chinese": {
        "Mandarin": ["AcadLang", "Chang1", "Chang2", "ChangPN", "ChangPlay", 
                    "Erbaugh", "LiReading", "LiZhou", "TCCM", "TCCM-reading",
                    "Tong", "Xinjiang", "Zhou1", "Zhou2", "Zhou3",
                    "ZhouAssessment", "ZhouDinner", "ZhouNarratives"],
        "Cantonese": ["HKU", "LeeWongLeung"]
    }
}

# Adapted from https://github.com/zoeyliu18/Negative_Constructions/

def get_existing_csvs(out_dir):
    """ Return a list of existing CSVs for a given collection and language
    """
    exists = []
    for file in os.listdir(out_dir):
        if file.endswith('.csv'):
            file = file.split('.')[0]
            exists.append(file)
    return exists

def write_csvs(collection, language, exists, out_dir):
    """ Write to CSVs the relevant data for a given collection and language, if that
    CSV does not already exist.
    """
    for corpus in COLLECTIONS[collection][language]:
        if corpus not in exists:
            data = cpy.get_utterances(corpus = corpus)
            data.to_csv(out_dir + corpus + ".csv")

def main(collection, language):
    """ Download then write the CSVs for a given collection and language
    """
    out_dir = "./corpora/{}/{}".format(collection, language)
    os.makedirs(out_dir, exist_ok=True)

    exists = get_existing_csvs(out_dir)
    write_csvs(collection, language, exists, out_dir)