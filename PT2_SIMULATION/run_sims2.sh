#!/bin/bash

# simset is the collection under which all simulations ran are stored
# simulations MUST be named simX for visualization to work

simset=set2_dyncl_repeat

# Canonical case
python3 main.py --NAME sim0 --SIMSET $simset 
python3 main.py --NAME sim1 --SIMSET $simset 
python3 main.py --NAME sim2 --SIMSET $simset 

python3 main.py --NAME sim3 --SIMSET $simset -C 50
python3 main.py --NAME sim4 --SIMSET $simset -C 50
python3 main.py --NAME sim5 --SIMSET $simset -C 50

python3 main.py --NAME sim6 --SIMSET $simset --FEAT_INIT variable
python3 main.py --NAME sim7 --SIMSET $simset --FEAT_INIT variable
python3 main.py --NAME sim8 --SIMSET $simset --FEAT_INIT variable

python3 main.py --NAME sim9 --SIMSET $simset --CLASS_INIT hierarchy multiple
python3 main.py --NAME sim10 --SIMSET $simset --CLASS_INIT hierarchy multiple
python3 main.py --NAME sim11 --SIMSET $simset --CLASS_INIT hierarchy multiple

python3 main.py --NAME sim12 --SIMSET $simset --CLASS_INIT hierarchy multiple --FEAT_INIT variable
python3 main.py --NAME sim13 --SIMSET $simset --CLASS_INIT hierarchy multiple --FEAT_INIT variable
python3 main.py --NAME sim14 --SIMSET $simset --CLASS_INIT hierarchy multiple --FEAT_INIT variable

# python3 merge.py --SIMSET $simset
python3 vis.py --SIMSET $simset