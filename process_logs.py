import json
import os
import re

from collections import defaultdict

root_dir = "results/"

tree = lambda: defaultdict(tree)
paths_tree = tree()

def process_log_file(path):
    output = {}
    with open(path, 'r') as f:
        contents = f.read().split("\n")
        model = None
        for line in contents:
            line = line.strip()
            if line.startswith("Results for model"):
                model = line.split()[-1]
                output[model] = {}
            elif line.startswith("accuracy"):
                accur = line.split()[-2]
                output[model]["accuracy"] = float(accur)
            elif line.startswith("macro avg"):
                macro = line.split()[-2]
                output[model]["macro_avg"] = float(macro)
            elif line.startswith("weighted avg"):
                weighted = line.split()[-2]
                output[model]["weighted_avg"] = float(weighted)
                model = None # reset model
    return output

for root, dirs, files in os.walk(root_dir):
    path_list = root.split(os.sep)
    current = paths_tree[path_list[0]]
    for item in path_list[1:]:
        current = current[item]
    for fname in files:
        contents = process_log_file(os.path.join(*(path_list+[fname])))
        current[fname] = contents

output_dict = json.loads(json.dumps(paths_tree))
print(output_dict)
