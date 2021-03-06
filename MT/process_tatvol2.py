'''
Process the TAT-Vol2 dataset into a format compatible with the trained MT model
'''
import glob, json, sys, re, os
from util import *

if len(sys.argv) < 3:
    print("usage: python process_tatvol2.py path/to/TAT-Vol2/json path/to/fairseq/raw_data/tatvol2.orig.nan")
    sys.exit(1)

tat_folder = sys.argv[1]
output_path = sys.argv[2]

files = sorted(glob.glob(f"{tat_folder}/**/*.json", recursive=True))
print(f"found {len(files)} files for tatvol2")

# NOTE: tatvol2 sentences are ordered by their file names in alphabetical order.
# This means e.g. xxx-6.9 comes after xxx-6.10

def process(line):
    return separate_punctuation(line)

out_sentences = []
out_sentence_ids = []
for fname in files:
    with open(fname) as f:
        res = process(json.load(f)['台羅數字調'])
        out_sentences.extend(res)
        out_sentence_ids.extend([f'{fname[19:]}\n'] * len(res))


with open(output_path, 'w') as f:
    f.writelines(out_sentences)

with open(output_path+".id", 'w') as f:
    f.writelines(out_sentence_ids)  