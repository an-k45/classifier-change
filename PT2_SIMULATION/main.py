import os
import argparse

import numpy as np
from tqdm import tqdm

class Child(object):
    def __init__(self, lexicon, C, F):
        self.lexicon = lexicon
        self.C = C  # no. classifiers in lexicon
        self.F = F  # no. features in lexicon
        self.classifier_count = np.zeros(self.C)  # no. seen occurences of each classifier
        self.classifier_features = np.zeros((self.C, self.F))  # no. feature observations with each classifier

    def add_interaction(self, cl_idx, noun_idx):
        self.classifier_count[cl_idx] += 1
        self.classifier_features[cl_idx] += self.lexicon.get_noun(noun_idx)

class Adult(object):
    def __init__(self, lexicon, C, F, initial_state):
        self.lexicon = lexicon
        self.C = C  # no. classifiers in lexicon
        self.F = F  # no. features in lexicon
        self.classifier_state = initial_state

    def get_pairable_classifiers_idxs(self, noun_idx):
        """ Given a noun index return the indices of pairable classifiers
        """
        diff = np.tile(self.lexicon.get_noun(noun_idx), (self.C, 1)) - self.classifier_state
        mins = np.min(diff, axis=1)
        min_idxs = np.argwhere(mins >= 0)
        return np.squeeze(min_idxs)

class Lexicon(object):
    def __init__(self, V, C, F, G, lex_dist_type, feature_hierarchy):
        self.V = V  # no. nouns in lexicon
        self.C = C  # no. classifiers in lexicon
        self.F = F  # no. features in lexicon
        self.G = G  # max no. features on a noun
        self.feature_hierarchy = feature_hierarchy
        
        self.lexicon_dist = self.init_lexicon_dist(lex_dist_type)
        self.nouns = self.init_nouns()

    def normalize(self, v):
        return v / np.sum(v)

    def init_lexicon_dist(self, lex_dist_type):
        if lex_dist_type == 'zipf':
            return self.normalize(np.array([self.V/(i+1) for i in range(self.V)]))
        elif lex_dist_type == 'uniform':
            return self.normalize(np.ones(self.V))

    def init_nouns(self):
        nouns = np.zeros((self.V, self.F))
        # TODO: numpy-ify this
        if self.feature_hierarchy is None:
            for i in range(self.V): 
                nouns[i][np.random.choice(self.F, self.G)] = 1
        else:
            for i in range(self.V):
                v = np.zeros(self.F)
                num_feats = np.random.choice(np.arange(1, self.G + 1))
                target_feats = np.random.choice(self.F, num_feats)
                for t in target_feats:
                    v[self.feature_hierarchy.get_features(t)] = 1
                nouns[i] += v
        return nouns 

    def get_random_noun_idxs(self, J):
        """ Return J randomly chosen indices for nouns based on the lexical distribution
        """
        return np.random.choice(self.V, J, p=self.lexicon_dist)

    def get_noun(self, i):
        return self.nouns[i]

class FeatureHierarchy(object):
    def __init__(self, F, B, feature_init):
        self.F = F  # no. features in lexicon
        self.B = B  # max branching factor on feature hierarchy
        self.feature_init = feature_init  # 'fixed', 'variable'

        self.feature_tree_ref = self.build_tree()
    
    def build_tree(self):
        tree_ref = {0: None}
        feats = list(range(self.F))
        stack = [feats.pop(0)]

        while len(stack) > 0:
            cur_parent = stack.pop(0)

            if len(feats) < self.B:
                children = feats
                for c in children:
                    tree_ref[c] = cur_parent
                break
            elif self.feature_init == 'fixed':
                children = feats[:self.B]
                feats = feats[self.B:]
            else:  # variable
                i = np.random.choice(np.arange(1, self.B + 1))
                children = feats[:i]
                feats = feats[i:]

            for c in children:
                tree_ref[c] = cur_parent
                stack.append(c)
        
        return tree_ref

    def get_features(self, feat):
        """ Given a feature return itself and all its ancestors
        """
        # print(self.feature_tree_ref)
        feats = []
        cur_feat = feat
        while cur_feat is not None:
            feats.append(cur_feat)
            cur_feat = self.feature_tree_ref[cur_feat]
        return np.array(feats)

class Simulation(object):
    def __init__(self, S, N, K, V, C, F, G, H, B, I, J, productive, lex_dist_type, classifier_init, feature_init):
        ### PARAMETERS ### 
        self.S = S  # no. total iterations in simulation

        self.N = N  # no. total individuals
        self.K = K  # no. children

        self.V = V  # no. nouns in lexicon
        self.C = C  # no. classifiers in lexicon
        self.F = F  # no. features in lexicon

        self.G = G  # max no. features on a noun
        self.H = H  # max no. features on a classifier
        self.B = B  # max branching factor on feature hierarchy

        self.I = I  # no. interactions each adult partakes in
        self.J = J  # no. lexical items drawn per interaction

        self.productive = productive  # method for productivity: 'TP' or 'majority'
        self.lex_dist_type = lex_dist_type  # Dist. type of nouns in lexicon: 'zipf' or 'uniform'
        # Method for classifier initialzation:
        # 'identity': Every classifier gets one unique feature
        # 'random': Random distribution of H features on each classifier
        # ['heirarchy',: Create a hierarchy of features, from F and B, where
        #    'single']: classifiers get one feature, including its parents
        #    'multiple']: classifiers get up to H features, including their parents
        self.classifier_init = classifier_init
        # Method for feature hierarchy initialization:
        # 'fixed': Each feature gets B subfeatures exactly
        # 'variable': Each feature gets between 1 and B subfeatures randomly
        self.feature_init = feature_init  # 'fixed', 'variable', None
        ### === ###

        ### STORAGE ###
        self.feature_metrics = []  # Store min, 25%tile, avg, 75%tile, max, of classifier features for each new adult
        self.duplicate_counts = []  # Store no. classifiers which are duplicates, column index = # features on classifier, regardless of combination of features (ie. different duplicates for same # features counted together)
        ### === ###
        
        ### SIMULATION INITIALIZATION ###
        self.feature_hierarchy = FeatureHierarchy(self.F, self.B, self.feature_init) if self.classifier_init[0] == 'hierarchy' else None
        self.lexicon = Lexicon(self.V, self.C, self.F, self.G, self.lex_dist_type, self.feature_hierarchy)
        self.children = self.init_children()
        self.adults = self.init_adults()
        self.init_start_state()
        ### === ###
    
    def init_productive_classifiers(self):
        if self.classifier_init == ["identity"]:
            assert self.C == self.F
            return np.identity(self.C)
        elif self.classifier_init == ["random"]:
            arr = np.array([0] * (self.F - self.H) + [1] * self.H)
            M = np.tile(arr, (self.C,1))

            x, y = M.shape
            rows = np.indices((x,y))[0]
            cols = [np.random.permutation(y) for _ in range(x)]
            return M[rows, cols]
            # return np.random.choice([0, 1], size=(self.C, self.F))
        elif self.classifier_init[0] == "hierarchy":
            M = np.zeros((self.C, self.F))
            
            v_0 = np.zeros(self.F)
            v_0[0] = 1  # ge4
            M[0] += v_0

            for i in range(1, self.C):
                v = np.zeros(self.F)
                if self.classifier_init[1] == "single":
                    v[self.feature_hierarchy.get_features(i % self.F)] = 1
                else:  # "multiple"
                    num_feats = np.random.choice(np.arange(1, self.H + 1))
                    target_feats = np.random.choice(self.F, num_feats)
                    for t in target_feats:
                        v[self.feature_hierarchy.get_features(t)] = 1
                M[i] += v
    
            return M

    def init_children(self):
        arr = []
        for _ in range(self.K):
            arr.append(Child(self.lexicon, self.C, self.F))
        return arr

    def init_adults(self):
        arr = []
        inital_state = self.init_productive_classifiers()
        for _ in range(self.N - self.K):
            arr.append(Adult(self.lexicon, self.C, self.F, inital_state))
        return arr
    
    def init_start_state(self):
        for k in tqdm(reversed(range(self.K))):  # Oldest to yonugest children
            for a in range(self.N - self.K):  # Adults
                targets = np.random.choice(self.K, self.I)  # Choose target interactions
                targets = targets[np.where(targets >= k)]
                for t in targets:
                    noun_idxs = self.lexicon.get_random_noun_idxs(self.J)  
                    for noun_idx in noun_idxs:  # Run interaction
                        cl_idxs = self.adults[a].get_pairable_classifiers_idxs(noun_idx)
                        if cl_idxs.size > 0:
                            if cl_idxs.size == 1:
                                cl_idx = cl_idxs
                            else:
                                cl_idx = np.random.choice(cl_idxs)
                            self.children[t].add_interaction(cl_idx, noun_idx)

    def adultify(self, child):
        counts = np.tile(child.classifier_count, (self.F, 1)).T
        if self.productive == 'majority':
            productivity = np.where(child.classifier_features >= (counts / 2), 1, 0)
        elif self.productive == 'TP':
            exceptions = counts - child.classifier_features
            tolerance = np.where(counts > 2, counts / np.log(counts), 0)  # TP breaks down when N <= 2. Also divide by zero stems here, but this is a pre-compute only, so not actually an issue.
            productivity = np.where(exceptions <= tolerance, 1, 0)

        # Restore classifiers which are not observed as 'dead'. These are otherwise set productive on every feature. 
        productivity[np.argwhere(child.classifier_count == 0)] = 0

        return Adult(self.lexicon, self.C, self.F, productivity)                    

    def simulate(self):
        """
        n individuals sorted by age (say, 100 or 1000?)
        k youngest are still learning (k for kid)
        The language has a vocab size v
        Each individual has their own grammar for these v items
        Vocab items follow a Zipfian frequency distribution <-- but we could vary it
        At every iteration,
           oldest individual "dies" and is removed from the set
           a new youngest individual is added
           Interaction takes place
           Everyone has i interactions with others 
                say 100 or 1000?
                At each interaction j vocab items are drawn from their frequency distribution
                     The youngest k learn from these interactions and update their representations
        """
        for s in tqdm(range(self.S)):  # Remove tqdm before commenting in print statements below 
            cl_state = self.adults[0].classifier_state

            # Information on number of features per classifier
            cl_num_feats = np.sum(cl_state, axis=1)
            self.feature_metrics.append([np.max(cl_num_feats), np.percentile(cl_num_feats, 75), np.mean(cl_num_feats), np.percentile(cl_num_feats, 25), np.min(cl_num_feats)])
            # print("ITER{} -- MIN: {}, MAX: {}, MEAN: {}".format(s, np.min(cl_num_feats), np.max(cl_num_feats), np.mean(cl_num_feats)))
            
            # Information on duplicate classifiers 
            u, indices, counts = np.unique(cl_state, axis=0, return_index=True, return_counts=True)
            cl_dup_num_feats = np.sum(cl_state[indices], axis=1)
            dups = np.zeros(self.F + 1)  # +1 for 0 feature case at index 0
            np.add.at(dups,
                      cl_dup_num_feats[np.argwhere(counts > 1).flatten()].astype(int),
                      counts[counts > 1].astype(int))
            self.duplicate_counts.append(dups)
            # print("ITER{}\n{}\n{}".format(s, counts, cl_dup_num_feats))

            # with np.printoptions(threshold=np.inf):
            #     print("ITER{}\n{}".format(s, cl_state))

            self.adults.pop()
            self.adults.insert(0, self.adultify(self.children.pop()))
            self.children.insert(0, Child(self.lexicon, self.C, self.F))

            for a in range(self.N - self.K):  # Adults
                targets = np.random.choice(self.K, self.I)  # Choose target interactions
                for t in targets:
                    noun_idxs = self.lexicon.get_random_noun_idxs(self.J)  
                    for noun_idx in noun_idxs:  # Run interaction
                        cl_idxs = self.adults[a].get_pairable_classifiers_idxs(noun_idx)
                        if cl_idxs.size > 0:
                            if cl_idxs.size == 1:
                                cl_idx = cl_idxs
                            else:
                                cl_idx = np.random.choice(cl_idxs)
                            self.children[t].add_interaction(cl_idx, noun_idx)

    def save(self, metrics, path, name):
        """ Save the values of metric to the given file at path
        """
        output = {}

        if "feature_metrics" in metrics:
            output[name + "_feature_metrics"] = np.array(self.feature_metrics)
        if "duplicate_counts" in metrics:
            output[name + "_duplicate_counts"] = np.array(self.duplicate_counts)

        np.savez(path, **output)

def main(args):
    print("======================================================")
    print("Running simulation: " + args.NAME)
    print("Parameters: " + str(vars(args)))

    # sim = Simulation(
    #     S=1000, 
    #     N=200, K=40, 
    #     V=1000, C=25, F=40, 
    #     G=4, H=3, B=3,
    #     I=5, J=5, 
    #     productive='TP', 
    #     lex_dist_type='zipf', 
    #     classifier_init=['hierarchy', 'single'],
    #     feature_init='fixed'
    # )

    sim = Simulation(
        S=args.S, 
        N=args.N, K=args.K, 
        V=args.V, C=args.C, F=args.F, 
        G=args.G, H=args.H, B=args.B,
        I=args.I, J=args.J, 
        productive=args.PROD, 
        lex_dist_type=args.LEX_TYPE, 
        classifier_init=args.CLASS_INIT,
        feature_init=args.FEAT_INIT
    )

    sim.simulate()

    out_dir = "./output/{}/data/".format(args.SIMSET)
    os.makedirs(out_dir, exist_ok=True)

    metrics = ["feature_metrics", "duplicate_counts"]
    sim.save(metrics, out_dir + args.NAME, args.NAME)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--NAME', type=str, required=True, help="Simulation name")
    parser.add_argument('--SIMSET', type=str, required=True, help="Simulation set name")

    parser.add_argument('-S', type=int, default=1000, help="No. simulations")

    parser.add_argument('-N', type=int, default=200, help="No. people")
    parser.add_argument('-K', type=int, default=40, help="No. children")
    
    parser.add_argument('-V', type=int, default=1000, help="No. nouns in lexicon")
    parser.add_argument('-C', type=int, default=25, help="No. classifiers in lexicon")
    parser.add_argument('-F', type=int, default=50, help="No. features in lexicon")

    parser.add_argument('-G', type=int, default=4, help="Max no. features on a noun")
    parser.add_argument('-H', type=int, default=3, help="Max no. features on a classifier")
    parser.add_argument('-B', type=int, default=3, help="Max branching factor on feature hierarchy")

    parser.add_argument('-I', type=int, default=5, help="No. interactions each adult partakes in")
    parser.add_argument('-J', type=int, default=5, help="No. lexical items drawn per interaction")

    parser.add_argument('--PROD', type=str, default='TP', help="Method for productivity")
    parser.add_argument('--LEX_TYPE', type=str, default='zipf', help="Dist. type of nouns in lexicon")
    parser.add_argument('--CLASS_INIT', nargs='+', default=['hierarchy', 'single'], help="Method for classifier initialzation")
    parser.add_argument('--FEAT_INIT', type=str, default='fixed', help="Method for feature hierarchy initialization")
    
    args = parser.parse_args()

    main(args)