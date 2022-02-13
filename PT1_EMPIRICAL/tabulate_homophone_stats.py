import argparse
import json
import re

syll_rx = re.compile("[0-9]")

def read_data(fname):
    with open(fname, "r") as f:
        return json.load(f)

def get_hstats(data):

    num_nouns = 0
    num_hphones = 0
    num_disambig_hphones = 0

    num_wordforms = 0
    num_hsets = 0
    num_disambig_hsets= 0
    num_fulldisambig_hsets = 0
    num_majority_disambig_hsets = 0 # TODO

    num_nountoks = 0
    num_hphonetoks = 0
    num_disambig_hphonetoks = 0
    num_fulldisambig_hphonetoks = 0
    num_majority_disambig_hphonetoks = 0 # TODO

    for wordform, words in data.items():
        wf_numsylls = len(syll_rx.findall(wordform))
        if not wf_numsylls: # skip words without tone marks
            continue
        num_wordforms += 1
        num_true = len(words.values())
        for word, cls in words.items():
            if len(word) != wf_numsylls: # excludes borrowed words and ones that are actually disambiguated by extra characters
                num_true -= 1
                continue
            num_nouns += 1

        cl_sets = []
        for word, cls in words.items(): # count the homophonous words
            if len(word) != wf_numsylls: 
                continue
            if num_true > 1:
                num_hphones += 1
            cl_sets.append(cls)

        if num_true > 1: # we know this wordform is homophonous 
            num_hsets += 1
            set_has_disambiguation = False
            set_fulldisambiguated = True
            for i, cl_seti in enumerate(cl_sets):
                is_disambiguated = False
                fulldisambiguated = True
                for j, cl_setj in enumerate(cl_sets):
                    if i == j: # don't compare against self
                        continue
                    if set(cl_seti.keys()).difference(set(cl_setj.keys())):
                        is_disambiguated = True
                    if set(cl_seti.keys()).difference(set(cl_setj.keys())) != set(cl_seti.keys()):
                        fulldisambiguated = False
                if is_disambiguated:
                    num_disambig_hphones += 1
                    set_has_disambiguation = True
                if not fulldisambiguated:
                    set_fulldisambiguated = False
            if set_has_disambiguation:
                num_disambig_hsets += 1
            if set_fulldisambiguated:
                num_fulldisambig_hsets += 1

        uniq_clsets = []
        for i, cl_seti in enumerate(cl_sets):
            is_disambiguated = False
            uniqclset = set(cl_seti.keys())
            for j, cl_setj in enumerate(cl_sets):
                if i == j:
                    continue
                uniqclset = uniqclset.difference(set(cl_setj.keys()))
            uniq_clsets.append(uniqclset)

        for clset, uniqclset in zip(cl_sets, uniq_clsets):
            for cl, count in clset.items():
                num_nountoks += count
                if num_true > 1:
                    num_hphonetoks += count
                    if cl in uniqclset:
                        num_disambig_hphonetoks += count
                        if len(uniqclset) == len(clset):
                            num_fulldisambig_hphonetoks += count

    return {"W":num_wordforms, "N":num_nouns, "H":num_hphones, "h":num_disambig_hphones, "K":num_hsets, "k_1":num_disambig_hsets, "k_full":num_fulldisambig_hsets, "k_2":num_majority_disambig_hsets, "N_t":num_nountoks, "H_t":num_hphonetoks, "h_t":num_disambig_hphonetoks, "h_tfull":num_fulldisambig_hphonetoks}



def display_hstats(hstats, infname):
    print("FILENAME:\t%s" % infname)
    print()
    print("TYPES:")
    print("W Number of wforms:\t\t\t\t\t%s" % hstats["W"])
    print("K Number of wforms w/ Homophones:\t\t\t%s" % hstats["K"])
    print("k_1 Number of wforms w/ Hphones Disambig'd by Cl:\t%s" % hstats["k_1"])
    print("k_full Number of '' '' '' fully Disambig'd by Cl:\t%s" % hstats["k_full"])
    print("Percent wforms w Hphones K/W\t\t\t\t%s%%" % round(hstats["K"]/hstats["W"]*100,3))
    print("Percent Hphone wforms Disambig'd k_1/K\t\t\t%s%%" % round(hstats["k_1"]/hstats["K"]*100,3))
    print("Percent wforms Disambig'd k_1/W\t\t\t\t%s%%" % round(hstats["k_1"]/hstats["W"]*100,3))
    print("Percent Hphone wforms '' k_full/K\t\t\t%s%%" % round(hstats["k_full"]/hstats["K"]*100,3))
    print("Percent wforms '' k_full/W\t\t\t\t%s%%" % round(hstats["k_full"]/hstats["W"]*100,3))
    print()
    print("TOKENS:")
    print("N Number of Noun Toks:\t\t\t\t\t%s" % hstats["N_t"])
    print("H Number of Nouns Toks w/ Homophones:\t\t\t%s" % hstats["H_t"])
    print("h Number of Nouns Toks w/ Hphones Disambig'd by Cl:\t%s" % hstats["h_t"])
    print("h_full Number of '' '' '' '' fully Disambig'd by Cl:\t%s" % hstats["h_tfull"])
    print("Percent Nouns Toks w/ Hphones H/N\t\t\t%s%%" % round(hstats["H_t"]/hstats["N_t"]*100,3))
    print("Percent Homophones Disambig'd h/H\t\t\t%s%%" % round(hstats["h_t"]/hstats["H_t"]*100,3))
    print("Percent Nouns Toks Disambig'd h/N\t\t\t%s%%" % round(hstats["h_t"]/hstats["N_t"]*100,3))
    print("Percent '' fully Disambig'd h_full/H\t\t\t%s%%" % round(hstats["h_tfull"]/hstats["H_t"]*100,3))
    print("Percent '' '' fully Disambig'd h_full/N\t\t\t%s%%" % round(hstats["h_tfull"]/hstats["N_t"]*100,3))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infname", type=str, help="Collection name")
    parser.add_argument("outfname", type=str, help="Language name")
    args = parser.parse_args()

    data = read_data(args.infname)
    hstats = get_hstats(data)
    display_hstats(hstats, args.infname)

#    dropnum = int(hstats["N_t"]/10)
    for i in range(0,10):
        hstats = get_hstats(data)
        display_hstats(hstats, args.infname)
