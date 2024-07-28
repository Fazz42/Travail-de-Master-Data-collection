import json
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score
from datetime import datetime

now = datetime.now()

with open('json/precision/Snomed_search.json', 'r') as f:
    predicted = json.load(f)

with open('json/precision/Snomed_search trié.json', 'r') as f:
    ground_truth = json.load(f)
precision_moyenne = []
precision_scores = {}
for key in predicted:
    if key in ground_truth and ground_truth[key] and predicted[key]:
        precision_scores[key] = len(ground_truth[key])/len(predicted[key])
        precision_moyenne.append(len(ground_truth[key])/len(predicted[key]))
        print(key, precision_scores[key])
    else:
        precision_scores[key] = None 
precision_moyenne = sum(precision_moyenne) / len(precision_moyenne)
print(precision_moyenne )

keys = list(precision_scores.keys())
values = list(precision_scores.values())
colors = ['skyblue' if value is not None else 'grey' for value in values]

fig, ax = plt.subplots()
bars = ax.bar(keys, [0 if value is None else value for value in values], color=colors)
ax.set_xlabel('Categories', fontsize=9)
ax.set_ylabel('Precision', fontsize=9)
ax.set_title('Precision for SNOMED CT Search', fontsize=12)
ax.set_xticklabels(keys, rotation=90, fontsize=9)

for i, value in enumerate(values):
    if value is None:
        bars[i].set_hatch('x')
        plt.text(i, 0.05, 'No data', ha='center', fontsize=8, color='grey', rotation=90)

plt.tight_layout()
plt.show()
plt.savefig("results/" + now.strftime("%Y%m%d%H%M") + "snomed_precision.pdf")
