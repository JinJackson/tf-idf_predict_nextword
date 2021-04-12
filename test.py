import json
from tqdm import tqdm
import pdb
with open('all_word_info.json', 'r', encoding='utf-8') as reader:
    all_data = {}
    lines = reader.readlines()
    for line in tqdm(lines):
        pos = line.index(':')
        key = line[:pos]
        value = json.loads(line[pos+1:])
        all_data[key] = value
    pdb.set_trace()
    print(all_data['经济'])

test = [1, 2, 3]

print(test[:10])