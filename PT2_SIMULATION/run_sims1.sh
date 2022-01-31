#!/bin/bash

# simset is the collection under which all simulations ran are stored
# simulations MUST be named simX for visualization to work

simset=set1_dyncl_sweep

# Canonical case
python3 main.py --NAME sim0 --SIMSET $simset

# Vary A and D
python3 main.py --NAME sim1 --SIMSET $simset -A 0.005
python3 main.py --NAME sim2 --SIMSET $simset -A 0.05
python3 main.py --NAME sim3 --SIMSET $simset -A 0.1

python3 main.py --NAME sim4 --SIMSET $simset -D 0.005
python3 main.py --NAME sim5 --SIMSET $simset -D 0.05
python3 main.py --NAME sim6 --SIMSET $simset -D 0.1

python3 main.py --NAME sim7 --SIMSET $simset -A 0.005 -D 0.005
python3 main.py --NAME sim8 --SIMSET $simset -A 0.05 -D 0.05
python3 main.py --NAME sim9 --SIMSET $simset -A 0.1 -D 0.1

# Repeat with random classifier dropping
python3 main.py --NAME sim10 --SIMSET $simset -A 0.005 --CLASS_DROP random
python3 main.py --NAME sim11 --SIMSET $simset -A 0.05 --CLASS_DROP random
python3 main.py --NAME sim12 --SIMSET $simset -A 0.1 --CLASS_DROP random

python3 main.py --NAME sim13 --SIMSET $simset -D 0.005 --CLASS_DROP random
python3 main.py --NAME sim14 --SIMSET $simset -D 0.05 --CLASS_DROP random
python3 main.py --NAME sim15 --SIMSET $simset -D 0.1 --CLASS_DROP random

python3 main.py --NAME sim16 --SIMSET $simset -A 0.005 -D 0.005 --CLASS_DROP random
python3 main.py --NAME sim17 --SIMSET $simset -A 0.05 -D 0.05 --CLASS_DROP random
python3 main.py --NAME sim18 --SIMSET $simset -A 0.1 -D 0.1 --CLASS_DROP random

# Repeat with variable feature initialization 
python3 main.py --NAME sim19 --SIMSET $simset -A 0.005 --FEAT_INIT variable
python3 main.py --NAME sim20 --SIMSET $simset -A 0.05 --FEAT_INIT variable
python3 main.py --NAME sim21 --SIMSET $simset -A 0.1 --FEAT_INIT variable

python3 main.py --NAME sim22 --SIMSET $simset -D 0.005 --FEAT_INIT variable
python3 main.py --NAME sim23 --SIMSET $simset -D 0.05 --FEAT_INIT variable
python3 main.py --NAME sim24 --SIMSET $simset -D 0.1 --FEAT_INIT variable

python3 main.py --NAME sim25 --SIMSET $simset -A 0.005 -D 0.005 --FEAT_INIT variable
python3 main.py --NAME sim26 --SIMSET $simset -A 0.05 -D 0.05 --FEAT_INIT variable
python3 main.py --NAME sim27 --SIMSET $simset -A 0.1 -D 0.1 --FEAT_INIT variable

# Repeat with multiple features selected per classifier 
python3 main.py --NAME sim28 --SIMSET $simset -A 0.005 --CLASS_INIT hierarchy multiple
python3 main.py --NAME sim29 --SIMSET $simset -A 0.05 --CLASS_INIT hierarchy multiple
python3 main.py --NAME sim30 --SIMSET $simset -A 0.1 --CLASS_INIT hierarchy multiple

python3 main.py --NAME sim31 --SIMSET $simset -D 0.005 --CLASS_INIT hierarchy multiple
python3 main.py --NAME sim32 --SIMSET $simset -D 0.05 --CLASS_INIT hierarchy multiple
python3 main.py --NAME sim33 --SIMSET $simset -D 0.1 --CLASS_INIT hierarchy multiple

python3 main.py --NAME sim34 --SIMSET $simset -A 0.005 -D 0.005 --CLASS_INIT hierarchy multiple
python3 main.py --NAME sim35 --SIMSET $simset -A 0.05 -D 0.05 --CLASS_INIT hierarchy multiple
python3 main.py --NAME sim36 --SIMSET $simset -A 0.1 -D 0.1 --CLASS_INIT hierarchy multiple

# python3 merge.py --SIMSET $simset
python3 vis.py --SIMSET $simset