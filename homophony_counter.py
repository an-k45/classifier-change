import childespy as cpy
from numpy.core.numeric import indices
import pandas as pd 
import os

CHILDREN = ["CHI", "CH2"]

CHINESE_EXCEPTIONS = [
    "那", "哪", "这", "几", "怎", "么",  # Determiners
    "〇", "零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "萬",  # Numbers
    "个", "只", "支", "本", "辆", "条", "张", "把", "层", "出", "次", "朵", "杆", "间", "件","架", "棵", "颗", "轮", "项", "张", "株", "对", "双", "些",  # Classifiers
    "块", "瓶", "杯"  # CL except when followed by "子"
]

EXCEPTIONS = {
    "Chinese": {
        "Mandarin": CHINESE_EXCEPTIONS,
        "Cantonese": CHINESE_EXCEPTIONS
    }
}

class EndLoop(Exception): 
    pass

def gather_utterances(data, syntax, want_children):
    """ Collect adult utterances with the syntactic categorical pattern cl n.
    Return the new data frame.
    """
    if want_children:
        data = data[data["speaker_code"].isin(CHILDREN)]
    else:
        data = data[~data["speaker_code"].isin(CHILDREN)]

    syntax = [s + "(?:[^a-z]|$)" for s in syntax]
    data = data[data["part_of_speech"].str.contains("|".join(syntax), na=False)]
    
    return data

def is_exception(s, collection, language):
    """ Return whether s is an exception (eg. not a noun in Chinese) or not.
    """
    return s in EXCEPTIONS[collection][language]

def get_cl_indices(POS, syntax):
    """ Return the indices of all classifiers in POS
    """
    noun_syntax = False if "[^n]" in syntax[0] else True

    if noun_syntax:
        indicies = [i for i in range(len(POS))
                    if (len(POS) > i + 1) and POS[i] == "cl" and POS[i + 1] == "n"
                    or (len(POS) > i + 2) and POS[i] == "cl" and POS[i + 1] == "adv" and POS[i + 2] == "n"
                    or (len(POS) > i + 2) and POS[i] == "cl" and POS[i + 1] == "adj" and POS[i + 2] == "n"]
    else:
        indicies = [i for i in range(len(POS))
                    if (len(POS) > i + 1) and POS[i] == "cl"
                    or (len(POS) > i + 2) and POS[i] == "cl" and POS[i + 1] == "adv"
                    or (len(POS) > i + 2) and POS[i] == "cl" and POS[i + 1] == "adj"]

    return indicies

def update_homophony_counter(counter, noun_phone, noun_symbol, classifier_phone):
    """ Update the homophony counter of the form
    {n_phone: {n_symbol: {c_phone: count}}}
    """
    if noun_phone not in counter:
        counter[noun_phone] = {}
    if noun_symbol not in counter[noun_phone]:
        counter[noun_phone][noun_symbol] = {}
    if classifier_phone not in counter[noun_phone][noun_symbol]:
        counter[noun_phone][noun_symbol][classifier_phone] = 0
    counter[noun_phone][noun_symbol][classifier_phone] += 1

def count_classifier_homophony(data, syntax):
    """ If classifiers are a system of communicative efficiency, then we expect
    nouns x_1 and x_2, with phonology y, to more often than not have different
    classifiers z_1 and z_2. 

    Return a dictionary of the form 
    {n_phone: {n_symbol: {c_phone: count}}}
    """
    counter = {}
    cl_phone_symbol_map = {}
    incongruent_list = []
    unresolved = []

    # Handle congruent cases, where we can directly index the classifier, and save incongruency for later
    for index, row in data.iterrows():
        POS = row["part_of_speech"].split()
        cl_indicies = get_cl_indices(POS, syntax)
        
        for i in cl_indicies:
            try:
                if len(row["gloss"].split()) == len(row["stem"].split()): 
                    noun_offset = 2 if (POS[i + 1] == "adv" or POS[i + 1] == "adj") else 1
                    noun_phone = row["stem"].split()[i + noun_offset]
                    noun_symbol = row["gloss"].split()[i + noun_offset]                    
                    classifier_phone = row["stem"].split()[i]
                    classifier_symbol = row["gloss"].split()[i]
                else:
                    incongruent_list.append(index)
                    continue
            except IndexError:
                unresolved.append(row)
                continue
            
            # Update classifier phone to symbol map
            if classifier_phone not in cl_phone_symbol_map:
                cl_phone_symbol_map[classifier_phone] = set([])
            cl_phone_symbol_map[classifier_phone].add(classifier_symbol)

            # TODO: Store row information, if necessary, instead of counts
            update_homophony_counter(counter, noun_phone, noun_symbol, classifier_phone)

    # Resolve incongruent cases by searching for the appropriate character manually, based on stored character-phone mappings. 
    for index, row in data.iterrows():
        if index in incongruent_list:
            POS = row["part_of_speech"].split()
            cl_indicies = get_cl_indices(POS, syntax)
            
            for i in cl_indicies:
                try:
                    noun_offset = 2 if (POS[i + 1] == "adv" or POS[i + 1] == "adj") else 1
                    noun_phone = row["stem"].split()[i + noun_offset]
                    classifier_phone = row["stem"].split()[i]
                except IndexError:
                    unresolved.append(row)
                    continue

                if classifier_phone in cl_phone_symbol_map:
                    cl_symbols = cl_phone_symbol_map[classifier_phone]
                else:
                    unresolved.append(row)
                    continue

                # TODO: Instead of iterating by index from 0...n, try a oscillating algorithm? 
                cl_symbol_index = None
                try:
                    for cl_s in cl_symbols:
                        gloss = row["gloss"].split()
                        for j in range(len(gloss)):
                            if gloss[j] == cl_s:
                                cl_symbol_index = j
                                raise EndLoop
                except EndLoop:
                    continue

                if cl_symbol_index:
                    try:
                        noun_symbol = row["gloss"].split()[cl_symbol_index + noun_offset]  # Possible noun_offset still buggy due to 'adv'. 
                    except IndexError:
                        unresolved.append(row)
                        continue
                else:
                    unresolved.append(row)
                    continue

                incongruent_list.remove(index)
                # TODO: Store row information, if necessary, instead of counts
                update_homophony_counter(counter, noun_phone, noun_symbol, classifier_phone)
    
    return counter, unresolved


def main(collection, language, syntax, want_children):
    path = "./corpora/{}/{}/".format(collection, language)

    data_cl = pd.DataFrame(columns=['id', 'gloss', 'stem', 'corpus_name', 'part_of_speech', 'speaker_code', 'collection_name'])
    for file in os.listdir(path):
        if file.endswith('.csv'):
            data = pd.read_csv(path + file).filter(items=['id', 'gloss', 'stem', 'corpus_name', 'part_of_speech', 'speaker_code', 'collection_name'], axis=1)
            data = gather_utterances(data, syntax, want_children)
            data_cl = data_cl.append(data, ignore_index=True)

    counter, unresolved = count_classifier_homophony(data_cl, syntax)
    return data_cl, counter, unresolved