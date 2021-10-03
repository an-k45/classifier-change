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

def get_existing_csvs(collection, language):
    """ Return a list of existing CSVs for a given collection and language
    """
    exists = []
    for file in os.listdir("./corpora/{}/{}".format(collection, language)):
        if file.endswith('.csv'):
            file = file.split('.')[0]
            exists.append(file)
    return exists

def write_csvs(collection, language, exists):
    """ Write to CSVs the relevant data for a given collection and language, if that
    CSV does not already exist.
    """
    output_path = "./corpora/{}/{}/".format(collection, language)
    for corpus in COLLECTIONS[collection][language]:
        if corpus not in exists:
            data = cpy.get_utterances(corpus = corpus)
            data.to_csv(output_path + corpus + ".csv")

def main(collection, language):
    """ Download then write the CSVs for a given collection and language
    """
    if "corpora" not in os.listdir("./"):
        os.mkdir("./corpora")
    
    if collection not in os.listdir("./corpora"):
        os.mkdir("./corpora/" + collection)
    
    if language not in os.listdir("./corpora/" + collection):
        os.mkdir("./corpora/{}/{}".format(collection, language))

    exists = get_existing_csvs(collection, language)
    write_csvs(collection, language, exists)