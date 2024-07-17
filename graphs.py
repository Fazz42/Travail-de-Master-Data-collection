import json
import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score

now = datetime.now()

# Fonction pour load les json
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Fonction pour choisir les json les plus récents
def get_latest_json(pattern, directory="json"):
    files = [f for f in os.listdir(directory) if re.match(pattern, f)]
    if not files:
        raise FileNotFoundError(f"Pas de {pattern} trouvé")
    files.sort(reverse=True)
    return os.path.join(directory, files[0])

# load des json les plus récent en appelant la fonction get_latest_json avec un pattern
ICD_search = load_json(get_latest_json(r"\d{12}ICD_search\.json"))
String_search_single = load_json(get_latest_json(r"\d{12}String_search_single\.json"))
String_search_multi = load_json(get_latest_json(r"\d{12}String_search_multi\.json"))
Snomed_search = load_json(get_latest_json(r"\d{12}Snomed_search\.json"))

# Function to calculate precision, recall, and F1 score
def calculate_stats(truth, results):
    all_stats = {}
    for key in truth:
        if key in results:
            y_true = set(truth[key])
            y_pred = set(results[key])
            tp = len(y_true & y_pred)
            fp = len(y_pred - y_true)
            fn = len(y_true - y_pred)
            precision = tp / (tp + fp) if tp + fp > 0 else 0
            recall = tp / (tp + fn) if tp + fn > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
            all_stats[key] = {
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "true_positive": tp,
                "false_positive": fp,
                "false_negative": fn
            }
        else:
            all_stats[key] = {
                "precision": 0,
                "recall": 0,
                "f1_score": 0,
                "true_positive": 0,
                "false_positive": 0,
                "false_negative": len(truth[key])
            }
    return all_stats

# Calculate statistics for search results 1 and 2
stats_1 = calculate_stats(ICD_search, Snomed_search)
stats_2 = calculate_stats(ICD_search, String_search_single)
stats_3 = calculate_stats(ICD_search, String_search_multi)

# Display statistics
def display_stats(stats, name):
    print(f"Statistics for {name}:")
    for key, value in stats.items():
        print(f"Category: {key}")
        print(f"  Precision: {value['precision']:.2f}")
        print(f"  Recall: {value['recall']:.2f}")
        print(f"  F1 Score: {value['f1_score']:.2f}")
        print(f"  True Positives: {value['true_positive']}")
        print(f"  False Positives: {value['false_positive']}")
        print(f"  False Negatives: {value['false_negative']}")
        print()

display_stats(stats_1, "Search Scheme 1")
display_stats(stats_2, "Search Scheme 2")
display_stats(stats_3, "Search Scheme 3")

# Plot precision in a histogram for comparison
def plot_precision_histogram(stats_1, stats_2, stats_3):
    categories = list(stats_1.keys())
    F1_1 = [stats_1[cat]['precision'] for cat in categories]
    F1_2 = [stats_2[cat]['precision'] for cat in categories]
    F1_3 = [stats_3[cat]['precision'] for cat in categories]

    x = range(len(categories))

    fig, ax = plt.subplots()
    ax.bar([xs-0.2 for xs in x], F1_1, width=0.2, label='Snomed CT', align='center')
    ax.bar(x, F1_2, width=0.2, label='String single', align='center')
    ax.bar([xs+0.2 for xs in x], F1_3, width=0.2, label='String multi', align='center')

    ax.set_xlabel('Categories')
    ax.set_ylabel('Precision')
    ax.set_title('Precision Comparison between Snomed CT, string search single and string search multi')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=90)
    ax.legend()

    plt.tight_layout()
    plt.show()
    plt.savefig("results/"+now.strftime("%Y%m%d%H%M")+"precision.pdf")

def plot_F1_histogram(stats_1, stats_2, stats_3):
    categories = list(stats_1.keys())
    F1_1 = [stats_1[cat]['f1_score'] for cat in categories]
    F1_2 = [stats_2[cat]['f1_score'] for cat in categories]
    F1_3 = [stats_3[cat]['f1_score'] for cat in categories]

    x = range(len(categories))

    fig, ax = plt.subplots()
    ax.bar([xs-0.2 for xs in x], F1_1, width=0.2, label='Snomed CT', align='center')
    ax.bar(x, F1_2, width=0.2, label='String single', align='center')
    ax.bar([xs+0.2 for xs in x], F1_3, width=0.2, label='String multi', align='center')

    ax.set_xlabel('Categories')
    ax.set_ylabel('F1 score')
    ax.set_title('F1 score Comparison between Snomed CT, string search single and string search multi')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=90)
    ax.legend()

    plt.tight_layout()
    plt.show()
    plt.savefig("results/"+now.strftime("%Y%m%d%H%M")+"f1_score.pdf")

# Plot data size in a histogram for comparison
def plot_data_size_histogram(ground_truth, results_1, results_2, results_3):
    categories = list(ground_truth.keys())
    size_truth = [len(ground_truth[cat]) for cat in categories]
    size_1 = [len(results_1[cat]) if cat in results_1 else 0 for cat in categories]
    size_2 = [len(results_2[cat]) if cat in results_2 else 0 for cat in categories]
    size_3 = [len(results_3[cat]) if cat in results_3 else 0 for cat in categories]

    x = range(len(categories))

    fig, ax = plt.subplots()
    ax.bar([xs-0.3 for xs in x], size_truth, width=0.2, label='ICD-10', align='center')
    ax.bar([xs-0.1 for xs in x], size_1, width=0.2, label='Snomed CT', align='center')
    ax.bar([xs+0.1 for xs in x], size_2, width=0.2, label='String single', align='center')
    ax.bar([xs+0.3 for xs in x], size_3, width=-0.2, label='String multi', align='center')

    ax.set_xlabel('Categories')
    ax.set_ylabel('Data Size')
    ax.set_title('Data Size Comparison between Ground Truth, Search Scheme 1, and 2')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=90)
    ax.legend()

    plt.tight_layout()
    plt.show()
    plt.savefig("results/"+now.strftime("%Y%m%d%H%M")+"datasize.pdf")

# Generate the plots
plot_precision_histogram(stats_1, stats_2, stats_3)
plot_F1_histogram(stats_1, stats_2, stats_3)
plot_data_size_histogram(ICD_search, Snomed_search, String_search_single, String_search_multi)