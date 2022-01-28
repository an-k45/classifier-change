#!/bin/bash

# simset is the collection under which all simulations ran are stored
# simulations MUST be named simX for visualization to work

simset=set1_dynclassifiers

# Canonical case
python3 main.py --NAME sim0 --SIMSET $simset 

# Non-hierarchical features
python3 main.py --NAME sim1 --SIMSET $simset --CLASS_INIT identity -C 50 -F 50
python3 main.py --NAME sim2 --SIMSET $simset --CLASS_INIT random

# Hierarchical with single feature selection
python3 main.py --NAME sim3 --SIMSET $simset --PROD majority

python3 main.py --NAME sim4 --SIMSET $simset -C 10
python3 main.py --NAME sim5 --SIMSET $simset -C 50

python3 main.py --NAME sim6 --SIMSET $simset -F 25
python3 main.py --NAME sim7 --SIMSET $simset -F 100

python3 main.py --NAME sim8 --SIMSET $simset -G 2
python3 main.py --NAME sim9 --SIMSET $simset -G 8

python3 main.py --NAME sim10 --SIMSET $simset -B 2
python3 main.py --NAME sim11 --SIMSET $simset -B 5

python3 main.py --NAME sim12 --SIMSET $simset -C 10 --FEAT_INIT variable
python3 main.py --NAME sim13 --SIMSET $simset -C 50 --FEAT_INIT variable

python3 main.py --NAME sim14 --SIMSET $simset -F 25 --FEAT_INIT variable
python3 main.py --NAME sim15 --SIMSET $simset -F 100 --FEAT_INIT variable

python3 main.py --NAME sim16 --SIMSET $simset -G 2 --FEAT_INIT variable
python3 main.py --NAME sim17 --SIMSET $simset -G 8 --FEAT_INIT variable

python3 main.py --NAME sim18 --SIMSET $simset -B 2 --FEAT_INIT variable
python3 main.py --NAME sim19 --SIMSET $simset -B 5 --FEAT_INIT variable

# Hierarchical with multiple feature selection
python3 main.py --NAME sim20 --SIMSET $simset --CLASS_INIT hierarchy multiple --PROD majority

python3 main.py --NAME sim21 --SIMSET $simset --CLASS_INIT hierarchy multiple -C 10
python3 main.py --NAME sim22 --SIMSET $simset --CLASS_INIT hierarchy multiple -C 50

python3 main.py --NAME sim23 --SIMSET $simset --CLASS_INIT hierarchy multiple -F 25
python3 main.py --NAME sim24 --SIMSET $simset --CLASS_INIT hierarchy multiple -F 100

python3 main.py --NAME sim25 --SIMSET $simset --CLASS_INIT hierarchy multiple -G 2
python3 main.py --NAME sim26 --SIMSET $simset --CLASS_INIT hierarchy multiple -G 8

python3 main.py --NAME sim27 --SIMSET $simset --CLASS_INIT hierarchy multiple -H 2
python3 main.py --NAME sim28 --SIMSET $simset --CLASS_INIT hierarchy multiple -H 5

python3 main.py --NAME sim29 --SIMSET $simset --CLASS_INIT hierarchy multiple -B 2
python3 main.py --NAME sim30 --SIMSET $simset --CLASS_INIT hierarchy multiple -B 5

python3 main.py --NAME sim31 --SIMSET $simset --CLASS_INIT hierarchy multiple -C 10 --FEAT_INIT variable
python3 main.py --NAME sim32 --SIMSET $simset --CLASS_INIT hierarchy multiple -C 50 --FEAT_INIT variable

python3 main.py --NAME sim33 --SIMSET $simset --CLASS_INIT hierarchy multiple -F 25 --FEAT_INIT variable
python3 main.py --NAME sim34 --SIMSET $simset --CLASS_INIT hierarchy multiple -F 100 --FEAT_INIT variable

python3 main.py --NAME sim35 --SIMSET $simset --CLASS_INIT hierarchy multiple -G 2 --FEAT_INIT variable
python3 main.py --NAME sim36 --SIMSET $simset --CLASS_INIT hierarchy multiple -G 8 --FEAT_INIT variable

python3 main.py --NAME sim37 --SIMSET $simset --CLASS_INIT hierarchy multiple -H 2 --FEAT_INIT variable
python3 main.py --NAME sim38 --SIMSET $simset --CLASS_INIT hierarchy multiple -H 5 --FEAT_INIT variable

python3 main.py --NAME sim39 --SIMSET $simset --CLASS_INIT hierarchy multiple -B 2 --FEAT_INIT variable
python3 main.py --NAME sim40 --SIMSET $simset --CLASS_INIT hierarchy multiple -B 5 --FEAT_INIT variable

# python3 merge.py --SIMSET $simset
python3 vis.py --SIMSET $simset