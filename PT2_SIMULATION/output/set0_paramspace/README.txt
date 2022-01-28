==== PARAMETER OVERVIEW ====
S: No. total iterations in sim

N: No. total individuals
K: No. children

V: No. nouns in lexicon
C: No. classifiers in lexicon
F: No. features in lexicon

G: Max no. features on a noun
H: Max no. features on a classifier
B: Max branching factor on feature hierarchy

I: No. interactions each adult partakes in
J: No. lexical items drawn per interaction

productive (PROD): Method for productivity ('TP' or 'majority')

lex_dist_type (LEX_TYPE): Dist. type of nouns in lexicon ('zipf' or 'uniform')

classifier_init (CLASS_INIT): Method for classifier initialization, where 
 - 'identity': Every classifier gets one unique feature
 - 'random': Random distribution of H features on each classifier
 - ['heirarchy',: Create a hierarchy of features, from F and B, where
 -  'single']: classifiers get one feature, including its parents
 -  'multiple']: classifiers get up to H features, including their parents

feature_init (FEAT_INIT): Method for feature hierarchy initialization, relevant only when classifier_init is a hierarchy, where
 - 'fixed': Each feature gets B subfeatures exactly
 - 'variable': Each feature gets between 1 and B subfeatures randomly

==== SIMULATIONS ====
The canonical simulation (sim0) is run on the following parameters:
S=1000, N=200, K=40, V=1000, C=25, F=50, G=4, H=3, B=3, I=5, J=5, PROD='TP', LEX_TYPE='zipf', CLASS_INIT=['hierarchy, 'single'], FEAT_INIT='fixed'


The varied parameter(s) for all other simulations are listed below.

# Non-hierarchical features
sim1: CLASS_INIT='identity', C=50, F=50 (C must equal F here)
sim2: CLASS_INIT='random'

# Hierarchical with single feature selection
sim3: PROD='majority'

sim4: C=10
sim5: C=50

sim6: F=25
sim7: F=100

sim8: G=2
sim9: G=8

sim10: B=2
sim11: B=5

sim12: C=10, FEAT_INIT='variable'
sim13: C=50, FEAT_INIT='variable'

sim14: F=25, FEAT_INIT='variable'
sim15: F=100, FEAT_INIT='variable'

sim16: G=2, FEAT_INIT='variable'
sim17: G=8, FEAT_INIT='variable'

sim18: B=2, FEAT_INIT='variable'
sim19: B=5, FEAT_INIT='variable'

# Hierarchical with multiple feature selection
sim20: CLASS_INIT=['hierarchy', 'multiple'], PROD='majority'

sim21: CLASS_INIT=['hierarchy', 'multiple'], C=10
sim22: CLASS_INIT=['hierarchy', 'multiple'], C=50

sim23: CLASS_INIT=['hierarchy', 'multiple'], F=25
sim24: CLASS_INIT=['hierarchy', 'multiple'], F=100

sim25: CLASS_INIT=['hierarchy', 'multiple'], G=2
sim26: CLASS_INIT=['hierarchy', 'multiple'], G=8

sim27: CLASS_INIT=['hierarchy', 'multiple'], H=2
sim28: CLASS_INIT=['hierarchy', 'multiple'], H=5

sim29: CLASS_INIT=['hierarchy', 'multiple'], B=2
sim30: CLASS_INIT=['hierarchy', 'multiple'], B=5

sim31: CLASS_INIT=['hierarchy', 'multiple'], C=10, FEAT_INIT='variable'
sim32: CLASS_INIT=['hierarchy', 'multiple'], C=50, FEAT_INIT='variable'

sim33: CLASS_INIT=['hierarchy', 'multiple'], F=25, FEAT_INIT='variable'
sim34: CLASS_INIT=['hierarchy', 'multiple'], F=100, FEAT_INIT='variable'

sim35: CLASS_INIT=['hierarchy', 'multiple'], G=2, FEAT_INIT='variable'
sim36: CLASS_INIT=['hierarchy', 'multiple'], G=8, FEAT_INIT='variable'

sim37: CLASS_INIT=['hierarchy', 'multiple'], H=2, FEAT_INIT='variable'
sim38: CLASS_INIT=['hierarchy', 'multiple'], H=5, FEAT_INIT='variable'

sim39: CLASS_INIT=['hierarchy', 'multiple'], B=2, FEAT_INIT='variable'
sim40: CLASS_INIT=['hierarchy', 'multiple'], B=5, FEAT_INIT='variable'
