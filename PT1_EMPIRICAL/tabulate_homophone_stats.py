import argparse
import json
import re
import random

random.seed("lchange'22")

syll_rx = re.compile("[0-9]")

def read_data(fname):
    with open(fname, "r") as f:
        return json.load(f)

def dropout(data, dropoutnum):
    while dropoutnum > 0:
        wordform, words = random.choice(list(data.items()))
        wf_numsylls = len(syll_rx.findall(wordform))
        if not wf_numsylls: # skip words without tone marks
            continue
        word, cls = random.choice(list(words.items()))
        if len(word) != wf_numsylls: # excludes borrowed words and ones that are actually disambiguated by extra characters
            continue
        cl, freq = random.choice(list(cls.items()))
        cls[cl] = freq-1

        # trim empties
        if cls[cl] == 0:
            del cls[cl]
        if len(words[word]) == 0:
            del words[word]
        if len(data[wordform]) == 0:
            del data[wordform]

        dropoutnum -= 1
    return data



def get_hstats(data):

    num_nouns = 0
    num_polysyll = 0
    num_hphones = 0
    num_disambig_hphones = 0

    num_wordforms = 0
    num_polysylls = 0
    num_hsets = 0
    num_disambig_hsets= 0
    num_fulldisambig_hsets = 0
    num_majority_disambig_hsets = 0 # TODO

    num_nountoks = 0
    num_polysylltoks = 0
    num_hphonetoks = 0
    num_disambig_hphonetoks = 0
    num_fulldisambig_hphonetoks = 0
    num_majority_disambig_hphonetoks = 0 # TODO

    clfreqs = {}

    for wordform, words in data.items():
        wf_numsylls = len(syll_rx.findall(wordform))
        if not wf_numsylls: # skip words without tone marks
            continue
        num_true = len(words.values())
        for word, cls in words.items():
            if len(word) != wf_numsylls: # excludes borrowed words and ones that are actually disambiguated by extra characters
                num_true -= 1
                continue
            num_nouns += 1
            if wf_numsylls > 1:
                num_polysyll += 1

        cl_sets = []
        if num_true >= 1:
            for word, cls in words.items(): 
                if len(word) != wf_numsylls: 
                    continue
                if num_true > 1:
                    num_hphones += 1
                cl_sets.append(cls)
                for cl in cls:
                    if cl not in clfreqs:
                        clfreqs[cl] = 0
                    clfreqs[cl] += cls[cl]
            if wf_numsylls > 1:
                num_polysylls += 1
            num_wordforms += 1

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
                    if wf_numsylls > 1:
                        num_polysylltoks += count
                    if num_true > 1:
                        num_hphonetoks += count
                        if cl in uniqclset:
                            num_disambig_hphonetoks += count
                            if len(uniqclset) == len(clset):
                                num_fulldisambig_hphonetoks += count

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

    return {"W":num_wordforms, "N":num_nouns, "H":num_hphones, "h":num_disambig_hphones, "K":num_hsets, "k_1":num_disambig_hsets, "k_full":num_fulldisambig_hsets, "k_2":num_majority_disambig_hsets, "N_t":num_nountoks, "H_t":num_hphonetoks, "h_t":num_disambig_hphonetoks, "h_tfull":num_fulldisambig_hphonetoks, "P":num_polysylls, "P_t":num_polysylltoks, "Cl":len(clfreqs), "Cl_t":sum(clfreqs.values())}



def display_hstats(hstats, infname):
    print("FILENAME:\t%s" % infname)
    print()
    print("TYPES:")
    print("Cl Number of classifiers:\t\t\t\t\t%s" % hstats["Cl"])
    print("W Number of wforms:\t\t\t\t\t%s" % hstats["W"])
    print("P Number of Polysyllabic wforms:\t\t\t%s\t%s" % (hstats["P"], round(hstats["P"]/hstats["W"]*100,6)))
    print("K Number of wforms w/ Homophones:\t\t\t%s" % hstats["K"])
    print("k_1 Number of wforms w/ Hphones Disambig'd by Cl:\t%s" % hstats["k_1"])
    print("k_full Number of '' '' '' fully Disambig'd by Cl:\t%s" % hstats["k_full"])
    print("Percent wforms w Hphones K/W\t\t\t\t%s%%" % round(hstats["K"]/hstats["W"]*100,6) if hstats["W"] else 0)
    print("Percent Hphone wforms Disambig'd k_1/K\t\t\t%s%%" % round(hstats["k_1"]/hstats["K"]*100,6) if hstats["K"] else 0)
    print("Percent wforms Disambig'd k_1/W\t\t\t\t%s%%" % round(hstats["k_1"]/hstats["W"]*100,6) if hstats["W"] else 0)
    print("Percent Hphone wforms '' k_full/K\t\t\t%s%%" % round(hstats["k_full"]/hstats["K"]*100,6) if hstats["K"] else 0)
    print("Percent wforms '' k_full/W\t\t\t\t%s%%" % round(hstats["k_full"]/hstats["W"]*100,6) if hstats["W"] else 0)
    print()
    print("TOKENS:")
    print("Cl_t Number of cl toks:\t\t\t\t\t%s" % hstats["Cl_t"])
    print("N Number of Noun Toks:\t\t\t\t\t%s" % hstats["N_t"])
    print("P_t Number of Polysyllabic Toks:\t\t\t%s\t%s" % (hstats["P_t"], round(hstats["P_t"]/hstats["N_t"]*100,6)))
    print("H Number of Nouns Toks w/ Homophones:\t\t\t%s" % hstats["H_t"])
    print("h Number of Nouns Toks w/ Hphones Disambig'd by Cl:\t%s" % hstats["h_t"])
    print("h_full Number of '' '' '' '' fully Disambig'd by Cl:\t%s" % hstats["h_tfull"])
    print("Percent Nouns Toks w/ Hphones H/N\t\t\t%s%%" % round(hstats["H_t"]/hstats["N_t"]*100,6) if hstats["N_t"] else 0)
    print("Percent Homophones Disambig'd h/H\t\t\t%s%%" % round(hstats["h_t"]/hstats["H_t"]*100,6) if hstats["H_t"] else 0)
    print("Percent Nouns Toks Disambig'd h/N\t\t\t%s%%" % round(hstats["h_t"]/hstats["N_t"]*100,6) if hstats["N_t"] else 0)
    print("Percent '' fully Disambig'd h_full/H\t\t\t%s%%" % round(hstats["h_tfull"]/hstats["H_t"]*100,6) if hstats["H_t"] else 0)
    print("Percent '' '' fully Disambig'd h_full/N\t\t\t%s%%" % round(hstats["h_tfull"]/hstats["N_t"]*100,6) if hstats["N_t"] else 0)


def write(f, trial, percent, hstats):
    fout.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (trial, percent,
                     hstats["W"],
                     hstats["K"],
                     hstats["k_1"],
                     hstats["k_full"],
                     hstats["K"]/hstats["W"] if hstats["W"] else 0,
                     hstats["k_1"]/hstats["W"] if hstats["W"] else 0,
                     hstats["k_1"]/hstats["K"] if hstats["K"] else 0,
                     hstats["k_full"]/hstats["W"] if hstats["W"] else 0,
                     hstats["k_full"]/hstats["K"] if hstats["K"] else 0,
                     hstats["N_t"],
                     hstats["H_t"],
                     hstats["h_t"],
                     hstats["h_tfull"],
                     hstats["H_t"]/hstats["N_t"] if hstats["N_t"] else 0,
                     hstats["h_t"]/hstats["N_t"] if hstats["N_t"] else 0,
                     hstats["h_t"]/hstats["H_t"] if hstats["H_t"] else 0,
                     hstats["h_tfull"]/hstats["N_t"] if hstats["N_t"] else 0,
                     hstats["h_tfull"]/hstats["H_t"] if hstats["H_t"] else 0,
                     ))



def limit_to_cantonese(infname, dropoutnum):
    print("DROPOUT:", dropoutnum)
    all_hstats = {"W":[], "N":[], "H":[], "h":[], "K":[], "k_1":[], "k_full":[], "k_2":[], "N_t":[], "H_t":[], "h_t":[], "h_tfull":[], "P":[], "P_t":[], "Cl":[], "Cl_t":[]}
    for trial in range (0,100):
#        print("Trial:", trial)
        data = read_data(args.infname)
        data = dropout(data, dropoutnum)
        hstats = get_hstats(data)
        for k, v in hstats.items():
            all_hstats[k].append(v)

    mean_hstats = {k:sum(v)/len(v) for k,v in all_hstats.items()}
    display_hstats(mean_hstats, infname)

def many_dropout_trials(infname):
    data = read_data(args.infname)
    hstats = get_hstats(data)
    with open(args.outfname, "w") as fout:
        fout.write("Trial,Percent,W,K,k,k_full,K/W,k/W,k/K,kfull/W,kfull/K,N,H,h,h_full,H/N,h/N,h/H,hfull/N,hfull/H\n")
        write(fout, 0,100,hstats)
        dropoutnum = int(hstats["N_t"]/10)
        for trial in range (1,101):
            print("Trial %s" % trial)
            for i in range(90,0,-10):
                data = dropout(data, dropoutnum)
                hstats = get_hstats(data)
                write(fout, trial, i, hstats)
    #            display_hstats(hstats, args.infname)
            data = read_data(args.infname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infname", type=str, help="Collection name")
    parser.add_argument("outfname", type=str, help="Language name")
    args = parser.parse_args()

    if "Mandarin" in args.infname:
        print("Limited Mandarin")
        dropoutnum = 11011 # DIFFERENCE BETWEEN NUM TOKS IN ADULT MANDARIN AND CANTONESE
        limit_to_cantonese(args.infname, dropoutnum)
        dropoutnum = 2825 # ACHIEVES CANTONESE TYPE COUNT
        limit_to_cantonese(args.infname, dropoutnum)

    data = read_data(args.infname)
    hstats = get_hstats(data)
    display_hstats(hstats, args.infname)

    

