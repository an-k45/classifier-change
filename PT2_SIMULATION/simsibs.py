import random
from math import log

random.seed("Alice and Bob")

IRRELEVANT = ""

def gen_zipflist(n):
    samplelist = []
    for i in range(0,n):
        samplelist.extend([i]*(int(n/(i+1))))
    return samplelist

def gen_reversezipflist(n):
    samplelist = []
    for i in range(0,n):
        samplelist.extend([n-i-1]*(int(n/(i+1))))
    return samplelist

def gen_reverseinverselist(n):
    samplelist = []
    for i in range(0,n):
        samplelist.extend([n-i-1]*(n-i))
    return samplelist


def gen_uniformlist(n):
    samplelist = []
    for i in range(0,n):
        samplelist.extend([i])
    return samplelist

def sample_n(samplelist, n):
    sampleds = []
    for i in range(0, n):
        samplei = random.randint(0,len(samplelist)-1)
        sampleds.append(samplelist[samplei])
    return sampleds

def applytp(variants, goodvar, evar):
    e = variants.count(evar)
    N = variants.count(goodvar) + e
    if N < 2:
        return False
    return e < N / log(N)

def learn(relevants, variants):
    tp0 = applytp(variants, 0, 1)
    tp1 = applytp(variants, 1, 0)
    other = -1
    if tp0:
        other = 0
    elif tp1:
        other = 1
#    print(tp0, tp1, other)
    learnedvariants = []
    numextended = 0
    for i, variant in enumerate(variants):
        if variant == 0 or variant == 1:
            learnedvariants.append(variant)
        elif i in relevants:
            learnedvariants.append(other)
            numextended += 1
        else:
            learnedvariants.append(IRRELEVANT)
#    if tp0:
#        print("TP 0, extended: ", numextended)
#        print(len(variants), len(learnedvariants), variants.count(IRRELEVANT), learnedvariants.count(IRRELEVANT), len(relevants))
#        print([v for v in variants if v != IRRELEVANT])
#        print([v for v in learnedvariants if v != IRRELEVANT])
    if tp1:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!TP 1, extended: ", numextended)
        print(len(variants), len(learnedvariants), variants.count(IRRELEVANT), learnedvariants.count(IRRELEVANT), len(relevants))
        print([v for v in variants if v != IRRELEVANT])
        print([v for v in learnedvariants if v != IRRELEVANT])

#        input("")
    return learnedvariants



class Lemmas(object):

    def __init__(self, N, relevants):
        self.N = N
        self.samplelist = gen_zipflist(N)
#        self.samplelist = gen_uniformlist(N)
        self.relevants = relevants

    def sample_n(self, n):
        return sample_n(self.samplelist, n)
        

class Individual(object):

    def __init__(self, lemmas, init_variants):
        self.lemmas = lemmas
        self.variants = init_variants
        self.inputvariants = {}

    def process_input(self, inputseq):
        for lemma, variant in inputseq:
            if lemma not in self.inputvariants:
                self.inputvariants[lemma] = []
            self.inputvariants[lemma].append(variant)

        categoricalvariants = [IRRELEVANT]*self.lemmas.N
        for i in self.lemmas.relevants:
            categoricalvariants[i] = -1
        for lemma, variants in self.inputvariants.items():
            categoricalvariants[lemma] = int(round(sum(variants),0)/len(variants))
#        print(self.variants)
#        print(categoricalvariants)
        self.variants = learn(self.lemmas.relevants, categoricalvariants)
#        print(sum(self.variants), self.variants)
#        print(" ")
#        input("")

            

class Community(object):

    def __init__(self, K, lemmas, init_variants):
        self.K = K
        self.lemmas = lemmas
        self.init_variants = set(init_variants)
        self.individuals = self.init_individuals(K,lemmas,init_variants)
#        self.samplelist = gen_uniformlist(K)
#        self.samplelist = gen_reversezipflist(K)
        self.samplelist = gen_reverseinverselist(K)
        
    def sample_n(self, n):
        return sample_n(self.samplelist, n)

    def init_individuals(self, K, lemmas, init_variants):
        N = lemmas.N
        indivs = []
        for i in range(0,K):
            indivlemmas = [IRRELEVANT]*N
            for n in lemmas.relevants:
                indivlemmas[n] = 0
            for e in init_variants:
                indivlemmas[e] = 1
            indivs.append(Individual(lemmas, indivlemmas))
        return indivs

    def get_input(self, n):
        inputseq = []
        while len(inputseq) < n: #so no got irrelevants or -1
            sampledindivs = self.sample_n(n)
            sampledlemmas = self.lemmas.sample_n(n)
            for i in range(0,n):
                indiv = self.individuals[sampledindivs[i]].variants
                lemma = sampledlemmas[i]
                variant = indiv[lemma]
                if variant == 0 or variant == 1:
                    inputseq.append((lemma, variant))
    #        print(inputseq)
        return inputseq


def create_individual(community, n):
    new_indiv = Individual(community.lemmas, [0]*community.lemmas.N)
    inputseq = community.get_input(n)
    new_indiv.process_input(inputseq)
    return new_indiv

def update_community(community, num_children, ncontinue, ninit):
    new_indiv = create_individual(community, ninit)
    for i, child in enumerate(reversed(community.individuals)):
        if i < num_children:
            inputseq = community.get_input(ncontinue)
            child.process_input(inputseq)
    community.individuals.append(new_indiv)
    community.individuals = community.individuals[1:]

def print_learner(community, indices, names):
    print("                     0  1")
    print("--------------------------")
    for index, name in zip(indices, names):
        variants = community.individuals[index].variants
        print(name, len(variants)-variants.count(-1)-variants.count(IRRELEVANT), variants.count(0), variants.count(1), [var for var in variants if var != IRRELEVANT])

def iterate(community, num_iters, num_children, ninit, ncontinue):

    for i in range(0,num_iters):
#        input("...")
        update_community(community, 3, 500, 1000)

    index = -1
    variants_mature = community.individuals[0-num_children-1].variants
    variants_young = community.individuals[-1].variants
#    print_learner(community, [-1,0-num_children-1], ["Young Learner:   ","Recently Matured:"])
#    print(" ")
    return community


def write_csv(f, data):
    for line in data:
        f.write(",".join([str(item) for item in line]) + "\n")



def freq_analysis(results, sample_indiv, num_iters):
    tokenfreqs_by_lemma = {}
    variants_by_lemma = {}
    finalstates_by_lemma = {}
    analyzedlemmas = []
    for community in results:
        print(community.init_variants)
        for i, individual in enumerate(community.individuals):
            for lemma, variants in individual.inputvariants.items():
                if lemma not in tokenfreqs_by_lemma:
                    tokenfreqs_by_lemma[lemma] = 0
                    variants_by_lemma[lemma] = []
                    finalstates_by_lemma[lemma] = []
                if i == sample_indiv: #only the last developing
                    tokenfreqs_by_lemma[lemma] += len(variants)
                    variants_by_lemma[lemma].append(int(round(sum(variants),0)/len(variants)))
    rank = 0
    prevfreq = 999999999
    for lemma, tokenfreq in sorted(tokenfreqs_by_lemma.items(),  key=lambda x: x[1], reverse=True):
        init_variant = "FALSE"
        if lemma in community.init_variants:
            init_variant = "TRUE"
            print(lemma, rank, tokenfreq/num_iters, variants_by_lemma[lemma], variants_by_lemma[lemma].count(1)/len(variants_by_lemma[lemma]))
        analyzedlemmas.append((len(community.init_variants), init_variant, lemma, rank, tokenfreq/num_iters, variants_by_lemma[lemma].count(1)/len(variants_by_lemma[lemma])))
        if prevfreq > tokenfreq:
            print("\t", prevfreq, tokenfreq, rank)
            rank += 1
        prevfreq = tokenfreq
    return analyzedlemmas


def run_experiment(num_lemmas, comm_size, num_children, ninit, ncontinue, relevants, init_variants, num_trials, num_iters):
    lemmas = Lemmas(num_lemmas,relevants)
    print("relevants: ", len(relevants), relevants)
    print("initial variants: ", len(init_variants), init_variants)
    spent_communities = []
    for i in range(0,num_trials):
        community = Community(comm_size, lemmas, init_variants)
        if i == 0:
            print_learner(community, [-1,], ["Initial:         ",])
            print("")
        print("Trial: ", i)
        spent_communities.append(iterate(community, num_iters=num_iters, num_children=num_children, ninit=ninit, ncontinue=ncontinue))
    return spent_communities

def exp_original():
    numlemmas = 1000
    comm_size = 100
    num_iters = 100
    num_children = 3
    ninit = numlemmas*10
    ncontinue = numlemmas*100
    ratio_relevants = 22.5 #22.5 and 2.7 for PGmc
    ratio_variants = 2.7
    relevants = [int(ratio_relevants*x) for x in range(0,int(numlemmas/ratio_relevants))]
    init_variants = [relevants[i] for i in [int(ratio_variants*x) for x in range(0,int(len(relevants)/ratio_variants))]]
    relevants = set(relevants)
    results = run_experiment(numlemmas, comm_size, num_children, ninit, ncontinue, relevants, init_variants, 50, num_iters)
    freq_analysis(results, comm_size-num_children-1, num_iters)


def exps_basic():

    def gen_relevants(ratio):
        return [int(ratio*x) for x in range(0,int(numlemmas/ratio))]

    def gen_init_variants(ratio, relevants):
        return [relevants[i] for i in [int(ratio*x) for x in range(0,int(len(relevants)/ratio))]]
    
    numlemmas = 100
    comm_size = 100
    num_children = 3
    num_iters = comm_size + num_children
    ninit = numlemmas*10
    ncontinue = numlemmas*100
    num_trials = 500

    ratios = [10,5]#,3,2]
    with open("exps_basic_invcom.csv", "w") as f:
        f.write("ratio,init_variant,lemma,tokenrank,tokenfreq,variant_rate\n")
        for ratio in ratios:
            print("RATIO", ratio)
            relevants = gen_relevants(1)
            init_variants = gen_init_variants(ratio, relevants)
            print(len(relevants), len(init_variants))
            relevants = set(relevants)
            results = run_experiment(numlemmas, comm_size, num_children, ninit, ncontinue, relevants, init_variants, num_trials, num_iters)
            analyzedlemmas = freq_analysis(results, comm_size-num_children-1, num_iters)
            write_csv(f, analyzedlemmas)


def exps_extension():
    return
            

def main():
#    exp_original()
    exps_basic()
    
if __name__=="__main__":
    main()
    
