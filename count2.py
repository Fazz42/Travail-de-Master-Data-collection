import json

with open('json/precision/ICD_search.json', 'r') as f:
    icd = json.load(f)

with open('json/precision/Snomed_search.json', 'r') as f:
    snomed = json.load(f)

    values_icd = sum(len(v) for v in icd.values())
    values_snomed = sum(len(v) for v in snomed.values())
    print("icd:", values_icd, "msnomed:", values_snomed)
