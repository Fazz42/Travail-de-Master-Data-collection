import json

with open('json/precision/String_search_single.json', 'r') as f:
    single = json.load(f)

with open('json/precision/String_search_multi.json', 'r') as f:
    multi = json.load(f)

    values_single = sum(len(v) for v in single.values())
    values_multi = sum(len(v) for v in multi.values())
    print("single:", values_single, "multi:", values_multi)
