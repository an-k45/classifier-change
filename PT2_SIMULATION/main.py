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
    def __init__(self, V, C, F, lex_dist_type):
        self.V = V  # no. nouns in lexicon
        self.C = C  # no. classifiers in lexicon
        self.F = F  # no. features in lexicon
        
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
        # Limit a noun to up to 3 features for now. 
        nouns = np.zeros((self.V, self.F))
        for i in range(self.V): # TODO: numpy-ify this
            nouns[i][np.random.choice(self.F, 3)] = 1
        return nouns 

    def get_random_noun_idxs(self, J):
        """ Return J randomly chosen indices for nouns based on the lexical distribution
        """
        return np.random.choice(self.V, J, p=self.lexicon_dist)

    def get_noun(self, i):
        return self.nouns[i]


class Simulation(object):
    def __init__(self, N, K, V, C, F, I, J, productive, lex_dist_type, classifier_init):
        """ Create feature sets, a set of nouns, and the initial generation.

        1. Setup
        1a. Devise sets of features, such that each feature has a set of subfeatures, to a finite depth.
        1b. Randomly(?) construct a large set of nouns with random(subject to some constraints?) features
        1c. Define GEN1 to consist of adults for whom all classifiers are productive. 
            Adults 'speak' by selecting any noun with equal probability*, 
            and selecting from valid classifiers with equal probability*.
        1d. Define GEN1 to consist of children who are pending input to determine 
            which classifiers are productive as per an acquisition model**.

        * Implement both uniform and Zipfian options
        ** Let's try TP and some kind of simple majority wins
        """
        self.N = N  # no. total individuals
        self.K = K  # no. children

        self.V = V  # no. nouns in lexicon
        self.C = C  # no. classifiers in lexicon
        self.F = F  # no. features in lexicon

        self.I = I  # no. interactions each adult partakes in
        self.J = J  # no. lexical items drawn per interaction

        self.productive = productive  # method for productivity: 'TP' or 'majority'
        self.lex_dist_type = lex_dist_type  # Dist. type of nouns in lexicon: 'zipf' or 'uniform'
        self.classifier_init = classifier_init  # Initial condition of classifiers: 'identity'
        
        self.lexicon = Lexicon(self.V, self.C, self.F, self.lex_dist_type)
        self.children = self.init_children()
        self.adults = self.init_adults()
        self.init_start_state()
    
    def init_productive_classifiers(self):
        if self.classifier_init == "identity":
            assert self.C == self.F
            return np.identity(self.C)

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
        for k in tqdm(reversed(range(self.K))):
            for a in range(self.N - self.K):
                targets = np.random.choice(self.K, self.I)
                targets = targets[np.where(targets >= k)]
                for t in targets:
                    # TODO: Select a noun via dist
                    noun_idxs = self.lexicon.get_random_noun_idxs(self.J)
                    for noun_idx in noun_idxs:
                        cl_idx = np.random.choice(self.adults[a].get_pairable_classifiers_idxs(noun_idx))
                        self.children[t].add_interaction(cl_idx, noun_idx)
                        

    def simulate():
        # n individuals sorted by age (say, 100 or 1000?)
        # k youngest are still learning (k for kid)
        # The language has a vocab size v
        # Each individual has their own grammar for these v items
        # Vocab items follow a Zipfian frequency distribution <-- but we could vary it
        # At every iteration,
        #    oldest individual "dies" and is removed from the set
        #    a new youngest individual is added
        #    Interaction takes place
        #    Everyone has i interactions with others 
        #         say 100 or 1000?
        #         At each interaction j vocab items are drawn from their frequency distribution
        #              The youngest k learn from these interactions and update their representations
        pass

