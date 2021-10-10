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
                num_feats = np.random.choice(np.arange(1, self.G))
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
                break
            elif self.feature_init == 'fixed':
                children = feats[:self.B]
                feats = feats[self.B:]
            else:  # variable
                i = np.random.choice(np.arange(1, self.B))
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
        self.classifier_init = classifier_init  # 'identity', 'random', ['hierarchy', 'single'/'multiple']
        self.feature_init = feature_init  # 'fixed', 'variable', None
        
        self.feature_hierarchy = FeatureHierarchy(self.F, self.B, self.feature_init) if self.classifier_init[0] == 'hierarchy' else None
        self.lexicon = Lexicon(self.V, self.C, self.F, self.G, self.lex_dist_type, self.feature_hierarchy)
        self.children = self.init_children()
        self.adults = self.init_adults()
        self.init_start_state()

        self.simulate()
    
    def init_productive_classifiers(self):
        if self.classifier_init == "identity":
            assert self.C == self.F
            return np.identity(self.C)
        elif self.classifier_init == "random":
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
                    v[self.feature_hierarchy.get_features(i)] = 1
                else:  # "multiple"
                    num_feats = np.random.choice(np.arange(1, self.H))
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
            productivity = np.where(child.classifier_features >= counts / 2, 1, 0)
            return Adult(self.lexicon, self.C, self.F, productivity)
        elif self.productive == 'TP':
            exceptions = counts - child.classifier_features
            tolerance = counts / np.log(counts)
            productivity = np.where(exceptions <= tolerance, 1, 0)
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
        for s in range(self.S):
            cl_f = np.sum(self.adults[0].classifier_state, axis=1)
            print("ITER{} -- MIN: {}, MAX: {}, MEAN: {}".format(s, np.min(cl_f), np.max(cl_f), np.mean(cl_f)))

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

def main():
    # classifier_init: 'identity', 'random', ['hierarchy', 'single'/'multiple']
    # feature_init: 'fixed', 'variable', None
    Simulation(S=500, 
               N=100, K=25, 
               V=1000, C=25, F=40, 
               G=2, H=2, B=3,
               I=5, J=5, 
               productive='TP', 
               lex_dist_type='zipf', 
               classifier_init=['hierarchy', 'single'],
               feature_init='fixed'
    )
    # Simulation(S=500, N=100, K=25, V=1000, C=25, F=25, G=3, H=2, I=5, J=5, productive='majority', lex_dist_type='zipf', classifier_init='identity')

if __name__ == "__main__":
    main()