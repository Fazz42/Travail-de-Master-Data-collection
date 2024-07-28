import json
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score
from datetime import datetime

now = datetime.now()

# Load dictionaries from JSON files
with open('json/precision/ICD_search.json', 'r') as f:
    predicted = json.load(f)

with open('json/precision/ICD_search trié.json', 'r') as f:
    ground_truth = json.load(f)

# Calculate precision for each key
precision_scores = {}
precision_moyenne = []
for key in predicted:
    if key in ground_truth and ground_truth[key] and predicted[key]:  # Check if there are values
        precision_scores[key] = len(ground_truth[key])/len(predicted[key])
        precision_moyenne.append(len(ground_truth[key])/len(predicted[key]))
    else:
        precision_scores[key] = None  # Indicate no data
precision_moyenne = sum(precision_moyenne) / len(precision_moyenne)
print(precision_moyenne )
# Plot the precision scores
keys = list(precision_scores.keys())
values = list(precision_scores.values())
colors = ['skyblue' if value is not None else 'grey' for value in values]

fig, ax = plt.subplots()
bars = ax.bar(keys, [0 if value is None else value for value in values], color=colors)
ax.set_xlabel('Categories', fontsize=9)
ax.set_ylabel('Precision', fontsize=9)
ax.set_title('Precision for ICD-10 Search', fontsize=12)
ax.set_xticklabels(keys, rotation=90, fontsize=9)

# Cross the keys with no data
for i, value in enumerate(values):
    if value is None:
        bars[i].set_hatch('x')
        plt.text(i, 0.05, 'No data', ha='center', fontsize=8, color='grey', rotation=90)

plt.tight_layout()
plt.show()
plt.savefig("results/" + now.strftime("%Y%m%d%H%M") + "icd_precision.pdf")
