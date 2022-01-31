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
The canonical simulation (sim0) is run on the following parameters:
S=1000, N=200, K=40, V=1000, C=25, F=50, G=4, H=3, B=3, I=5, J=5, A=0.01, D=0.01,
PROD='TP', LEX_TYPE='zipf', CLASS_INIT=['hierarchy, 'single'], FEAT_INIT='fixed', CLASS_DROP='general'

The varied parameter(s) for all other simulations are listed below.

# Vary A and D
sim1: -A 0.005
sim2: -A 0.05
sim3: -A 0.1

sim4: -D 0.005
sim5: -D 0.05
sim6: -D 0.1

sim7: -A 0.005 -D 0.005
sim8: -A 0.05 -D 0.05
sim9: -A 0.1 -D 0.1

# Repeat with random classifier dropping
sim10: -A 0.005 --CLASS_DROP random
sim11: -A 0.05 --CLASS_DROP random
sim12: -A 0.1 --CLASS_DROP random

sim13: -D 0.005 --CLASS_DROP random
sim14: -D 0.05 --CLASS_DROP random
sim15: -D 0.1 --CLASS_DROP random

sim16: -A 0.005 -D 0.005 --CLASS_DROP random
sim17: -A 0.05 -D 0.05 --CLASS_DROP random
sim18: -A 0.1 -D 0.1 --CLASS_DROP random

# Repeat with variable feature initialization 
sim19: -A 0.005 --FEAT_INIT variable
sim20: -A 0.05 --FEAT_INIT variable
sim21: -A 0.1 --FEAT_INIT variable

sim22: -D 0.005 --FEAT_INIT variable
sim23: -D 0.05 --FEAT_INIT variable
sim24: -D 0.1 --FEAT_INIT variable

sim25: -A 0.005 -D 0.005 --FEAT_INIT variable
sim26: -A 0.05 -D 0.05 --FEAT_INIT variable
sim27: -A 0.1 -D 0.1 --FEAT_INIT variable

# Repeat with multiple features selected per classifier 
sim28: -A 0.005 --CLASS_INIT hierarchy multiple
sim29: -A 0.05 --CLASS_INIT hierarchy multiple
sim30: -A 0.1 --CLASS_INIT hierarchy multiple

sim31: -D 0.005 --CLASS_INIT hierarchy multiple
sim32: -D 0.05 --CLASS_INIT hierarchy multiple
sim33: -D 0.1 --CLASS_INIT hierarchy multiple

sim34: -A 0.005 -D 0.005 --CLASS_INIT hierarchy multiple
sim35: -A 0.05 -D 0.05 --CLASS_INIT hierarchy multiple
sim36: -A 0.1 -D 0.1 --CLASS_INIT hierarchy multiple
