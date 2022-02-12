#!/bin/bash

# Generate counters for homophony
# Mandarin adults
python3 main.py -C Chinese -L Mandarin -T adult -S all
python3 main.py -C Chinese -L Mandarin -T adult -S noun
python3 main.py -C Chinese -L Mandarin -T adult -S num_noun
python3 main.py -C Chinese -L Mandarin -T adult -S dem_noun
python3 main.py -C Chinese -L Mandarin -T adult -S det_noun
python3 main.py -C Chinese -L Mandarin -T adult -S not_noun

# Mandarin children
python3 main.py -C Chinese -L Mandarin -T child -S all
python3 main.py -C Chinese -L Mandarin -T child -S noun
python3 main.py -C Chinese -L Mandarin -T child -S num_noun
python3 main.py -C Chinese -L Mandarin -T child -S dem_noun
python3 main.py -C Chinese -L Mandarin -T child -S det_noun
python3 main.py -C Chinese -L Mandarin -T child -S not_noun

# Cantonese adults
python3 main.py -C Chinese -L Cantonese -T adult -S all
python3 main.py -C Chinese -L Cantonese -T adult -S noun
python3 main.py -C Chinese -L Cantonese -T adult -S num_noun
python3 main.py -C Chinese -L Cantonese -T adult -S dem_noun
python3 main.py -C Chinese -L Cantonese -T adult -S det_noun
python3 main.py -C Chinese -L Cantonese -T adult -S not_noun

# Cantonese children
python3 main.py -C Chinese -L Cantonese -T child -S all
python3 main.py -C Chinese -L Cantonese -T child -S noun
python3 main.py -C Chinese -L Cantonese -T child -S num_noun
python3 main.py -C Chinese -L Cantonese -T child -S dem_noun
python3 main.py -C Chinese -L Cantonese -T child -S det_noun
python3 main.py -C Chinese -L Cantonese -T child -S not_noun


# Select out subsets 
python3 parse_main_output.py -cl
python3 parse_main_output.py -hom