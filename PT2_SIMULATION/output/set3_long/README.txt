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

A: Probability [0,1] a new classifier is added, given an opening
D: Probability [0,1] a classifier is dropped

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

classifier_drop (CLASS_DROP): Method for dropping classifiers ('general' or 'random')

==== SIMULATIONS ====
The canonical simulation is run on the following parameters:
S=1000, N=200, K=40, V=1000, C=25, F=50, G=4, H=3, B=3, I=5, J=5, A=0.01, D=0.01,
PROD='TP', LEX_TYPE='zipf', CLASS_INIT=['hierarchy, 'single'], FEAT_INIT='fixed', CLASS_DROP='general'

The varied parameter(s) for all other simulations are listed below.

sim0: -S 5000
sim1: -S 5000
sim2: -S 5000
sim3: -S 5000
sim4: -S 5000
