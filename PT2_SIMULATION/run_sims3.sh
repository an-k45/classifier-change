#!/bin/bash

# simset is the collection under which all simulations ran are stored
# simulations MUST be named simX for visualization to work

simset=set3_long

# Canonical case
python3 main.py --NAME sim0 --SIMSET $simset -S 5000
python3 main.py --NAME sim1 --SIMSET $simset -S 5000
python3 main.py --NAME sim2 --SIMSET $simset -S 5000
python3 main.py --NAME sim3 --SIMSET $simset -S 5000
python3 main.py --NAME sim4 --SIMSET $simset -S 5000

# More classifiers
python3 main.py --NAME sim5 --SIMSET $simset -S 5000 -C 50
python3 main.py --NAME sim6 --SIMSET $simset -S 5000 -C 50
python3 main.py --NAME sim7 --SIMSET $simset -S 5000 -C 50
python3 main.py --NAME sim8 --SIMSET $simset -S 5000 -C 50
python3 main.py --NAME sim9 --SIMSET $simset -S 5000 -C 50

# More mutations
python3 main.py --NAME sim10 --SIMSET $simset -S 5000 -A 0.05 -D 0.05
python3 main.py --NAME sim11 --SIMSET $simset -S 5000 -A 0.05 -D 0.05
python3 main.py --NAME sim12 --SIMSET $simset -S 5000 -A 0.05 -D 0.05
python3 main.py --NAME sim13 --SIMSET $simset -S 5000 -A 0.05 -D 0.05
python3 main.py --NAME sim14 --SIMSET $simset -S 5000 -A 0.05 -D 0.05

# python3 merge.py --SIMSET $simset
python3 vis.py --SIMSET $simset