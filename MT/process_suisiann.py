'''
Process the SiuSann dataset into a format compatible with the trained MT model
Known issue: will add tone 1 or 4 to non-Taiwanese (e.g. English) words
'''
import sys, re
import pandas as pd
import epitran

if len(sys.argv) < 3:
    print("usage: python process_siusann.py path/to/SiuSann.csv path/to/fairseq/raw_data/all.orig.nan")
    sys.exit(1)

siusann_path = sys.argv[1]
output_path = sys.argv[2]
try:
    epi = epitran.Epitran('temp-nan', tones=True)
except KeyError:
    print("You are probably using the official Epitran. Please install our fork from https://github.com/kalvinchang/epitran-temp")
    sys.exit(1)


def diacritics2numbers(line):
    line = re.sub(r'([,.?!:-])', r" \1 ", line)

    punc = {'SP', ',', '.', '?', '!', ':', '-', '"'}
    words = line.split()
    for i in range(len(words)):
        if words[i] not in punc:
            words[i] = epi.transliterate(words[i])

    line = ' '.join(words)

    # then recover by replacing punctuation with the space removed
    # line = re.sub(r'SP', r" SP ", line)
    # only replace dash
    line = re.sub(r' (-) ', r"\1", line)
    # the double dash does not have a dash preceding it
    line = re.sub(r'(--) ', r"\1", line)
    return line


sentences = pd.read_csv(siusann_path)['羅馬字'].to_list()
out_sentences = [diacritics2numbers(sent)+'\n' for sent in sentences]

with open(output_path, 'w') as f:
    f.writelines(out_sentences)