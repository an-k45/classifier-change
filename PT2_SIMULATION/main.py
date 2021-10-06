class Child(object):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.classifier_count = {}  # no. seen occurences of each classifier
        self.classifier_features = {}  # no. feature observations with each classifier

# Child view of classifier for TP:
# C1 = {"total": 10, "a": 7, "b": 3, "c": 1} --> n=10, then total count of appearence of features a,b,c with C1 via a noun

class Adult(object):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.classifiers = {}

class Lexicon(object):
    def __init__(self, V, lexicon_dist):
        super().__init__()

class Simulation(object):
    def __init__(self, N, K, V, I, J, productive, lexicon_dist):
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
        self.I = I  # no. interactions each adult partakes in
        self.J = J  # no. lexical items drawn per interaction

        self.productive = productive  # method for productivity
        self.lexicon_dist = lexicon_dist  # Dist. type of nouns in lexicon
        assert self.productive in ["TP", "majority"]
        
        self.lexicon = Lexicon(self.V, self.lexicon_dist)
        self.children = self.init_children(K, self.lexicon)
        self.adults = self.init_adults(N - K, self.lexicon)
    
    def init_children(self, num, lexicon):
        pass

    def init_adults(self, num, lexicon):
        pass

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

