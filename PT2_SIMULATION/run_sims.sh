#!/bin/bash

# Canonical case
python3 main.py --NAME sim0 

# Non-hierarchical features
python3 main.py --NAME sim1 --CLASS_INIT identity -C 50 -F 50
python3 main.py --NAME sim2 --CLASS_INIT random

# Hierarchical with single feature selection
python3 main.py --NAME sim3 --PROD majority

python3 main.py --NAME sim4 -C 10
python3 main.py --NAME sim5 -C 50

python3 main.py --NAME sim6 -F 25
python3 main.py --NAME sim7 -F 100

python3 main.py --NAME sim8 -G 2
python3 main.py --NAME sim9 -G 8

python3 main.py --NAME sim10 -B 2
python3 main.py --NAME sim11 -B 5

python3 main.py --NAME sim12 -C 10 --FEAT_INIT variable
python3 main.py --NAME sim13 -C 50 --FEAT_INIT variable

python3 main.py --NAME sim14 -F 25 --FEAT_INIT variable
python3 main.py --NAME sim15 -F 100 --FEAT_INIT variable

python3 main.py --NAME sim16 -G 2 --FEAT_INIT variable
python3 main.py --NAME sim17 -G 8 --FEAT_INIT variable

python3 main.py --NAME sim18 -B 2 --FEAT_INIT variable
python3 main.py --NAME sim19 -B 5 --FEAT_INIT variable

# Hierarchical with multiple feature selection
python3 main.py --NAME sim20 --CLASS_INIT hierarchy multiple --PROD majority

python3 main.py --NAME sim21 --CLASS_INIT hierarchy multiple -C 10
python3 main.py --NAME sim22 --CLASS_INIT hierarchy multiple -C 50

python3 main.py --NAME sim23 --CLASS_INIT hierarchy multiple -F 25
python3 main.py --NAME sim24 --CLASS_INIT hierarchy multiple -F 100

python3 main.py --NAME sim25 --CLASS_INIT hierarchy multiple -G 2
python3 main.py --NAME sim26 --CLASS_INIT hierarchy multiple -G 8

python3 main.py --NAME sim27 --CLASS_INIT hierarchy multiple -H 2
python3 main.py --NAME sim28 --CLASS_INIT hierarchy multiple -H 5

python3 main.py --NAME sim29 --CLASS_INIT hierarchy multiple -B 2
python3 main.py --NAME sim30 --CLASS_INIT hierarchy multiple -B 5

python3 main.py --NAME sim31 --CLASS_INIT hierarchy multiple -C 10 --FEAT_INIT variable
python3 main.py --NAME sim32 --CLASS_INIT hierarchy multiple -C 50 --FEAT_INIT variable

python3 main.py --NAME sim33 --CLASS_INIT hierarchy multiple -F 25 --FEAT_INIT variable
python3 main.py --NAME sim34 --CLASS_INIT hierarchy multiple -F 100 --FEAT_INIT variable

python3 main.py --NAME sim35 --CLASS_INIT hierarchy multiple -G 2 --FEAT_INIT variable
python3 main.py --NAME sim36 --CLASS_INIT hierarchy multiple -G 8 --FEAT_INIT variable

python3 main.py --NAME sim37 --CLASS_INIT hierarchy multiple -H 2 --FEAT_INIT variable
python3 main.py --NAME sim38 --CLASS_INIT hierarchy multiple -H 5 --FEAT_INIT variable

python3 main.py --NAME sim39 --CLASS_INIT hierarchy multiple -B 2 --FEAT_INIT variable
python3 main.py --NAME sim40 --CLASS_INIT hierarchy multiple -B 5 --FEAT_INIT variable

python3 merge.py
python3 vis.py