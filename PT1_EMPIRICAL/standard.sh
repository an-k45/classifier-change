#!/bin/bash

# Mandarin adults
python3 main.py -c Chinese -l Mandarin -ch n -s all
python3 main.py -c Chinese -l Mandarin -ch n -s noun
python3 main.py -c Chinese -l Mandarin -ch n -s num_noun
python3 main.py -c Chinese -l Mandarin -ch n -s dem_noun
python3 main.py -c Chinese -l Mandarin -ch n -s det_noun
python3 main.py -c Chinese -l Mandarin -ch n -s not_noun

# Mandarin children
python3 main.py -c Chinese -l Mandarin -ch y -s all
python3 main.py -c Chinese -l Mandarin -ch y -s noun
python3 main.py -c Chinese -l Mandarin -ch y -s num_noun
python3 main.py -c Chinese -l Mandarin -ch y -s dem_noun
python3 main.py -c Chinese -l Mandarin -ch y -s det_noun
python3 main.py -c Chinese -l Mandarin -ch y -s not_noun

# Cantonese adults
python3 main.py -c Chinese -l Cantonese -ch n -s all
python3 main.py -c Chinese -l Cantonese -ch n -s noun
python3 main.py -c Chinese -l Cantonese -ch n -s num_noun
python3 main.py -c Chinese -l Cantonese -ch n -s dem_noun
python3 main.py -c Chinese -l Cantonese -ch n -s det_noun
python3 main.py -c Chinese -l Cantonese -ch n -s not_noun

# Cantonese children
python3 main.py -c Chinese -l Cantonese -ch y -s all
python3 main.py -c Chinese -l Cantonese -ch y -s noun
python3 main.py -c Chinese -l Cantonese -ch y -s num_noun
python3 main.py -c Chinese -l Cantonese -ch y -s dem_noun
python3 main.py -c Chinese -l Cantonese -ch y -s det_noun
python3 main.py -c Chinese -l Cantonese -ch y -s not_noun