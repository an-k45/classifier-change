#!/bin/bash

# Mandarin adults
python3 main.py Chinese Mandarin no noun_all
python3 main.py Chinese Mandarin no num
python3 main.py Chinese Mandarin no dem
python3 main.py Chinese Mandarin no det
python3 main.py Chinese Mandarin no not_noun_all

# Mandarin children
python3 main.py Chinese Mandarin yes noun_all
python3 main.py Chinese Mandarin yes num
python3 main.py Chinese Mandarin yes dem
python3 main.py Chinese Mandarin yes det
python3 main.py Chinese Mandarin yes not_noun_all

# Cantonese adults
python3 main.py Chinese Cantonese no noun_all
python3 main.py Chinese Cantonese no num
python3 main.py Chinese Cantonese no dem
python3 main.py Chinese Cantonese no det
python3 main.py Chinese Cantonese no not_noun_all

# Cantonese children
python3 main.py Chinese Cantonese yes noun_all
python3 main.py Chinese Cantonese yes num
python3 main.py Chinese Cantonese yes dem
python3 main.py Chinese Cantonese yes det
python3 main.py Chinese Cantonese yes not_noun_all