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

# python3 merge.py --SIMSET $simset
python3 vis.py --SIMSET $simset