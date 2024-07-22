import requests
import json
import pandas as pd
from datetime import datetime
import re


URL = 'http://localhost:8080/MAIN/concepts?ecl='

def get_results_from_ecl(ecl):
    response = requests.get(URL + ecl).json()
    response_agg = requests.get(URL + ecl).json()
    while 'searchAfter' in response:
        search_after = response['searchAfter']
        response_next = requests.get(URL + ecl + '&searchAfter=' + search_after).json()
        # append new page to response.json()
        response_agg['items'].extend(response_next['items'])
        response = response_next
    return response_agg


def hugdata():
    hug_data = {}
    for index, row in df0.iterrows():
        num = re.findall(r'\d+', str(row['SNOMED_CT_MULT']))
        for i in num:
            if i in hug_data.keys():
                hug_data[i].append(row['HUG_LABEL_FR'])
            else:
                hug_data[i] = [row['HUG_LABEL_FR']]
    f = open("json/hug_data.json","w")
    json.dump(hug_data, f)


def snomed(df1, hug_data, df5):
    now = datetime.now()
    query_ecl_dict = {}
    for id, i in enumerate(df5.iloc):
        ecl = i["ecl_query"]
        if isinstance(ecl, str):
            ecl_res=get_results_from_ecl(str(ecl))
            query_ecl_dict[i["sous-question"]] = [it['conceptId'] for it in ecl_res['items']]
    f = open("json/"+now.strftime("%Y%m%d%H%M")+"Step1_api_ecl.json","w")
    json.dump(query_ecl_dict, f)
    print("étape 1")

    dict_label_ecl = {}
    for key, value in query_ecl_dict.items():
        cid_set = set()
        for item in value:
            if item in hug_data:
                cid_set.update(hug_data[item])
        dict_label_ecl[key]=list(cid_set)
    f = open("json/"+now.strftime("%Y%m%d%H%M")+"Snomed_search.json","w")
    json.dump(dict_label_ecl, f)
    print("étape 2")


def string_search_single(df0, df2):
    now = datetime.now()
    hug_label = [row["HUG_LABEL_FR"].lower() for index, row in df0.iterrows()]

    dict_string = {}
    for index, row in df2.iterrows():
        for i in hug_label:
            if str(row["string"]).lower() in i:
                if row["sous-question"] in dict_string:
                    dict_string[row["sous-question"]].append(i)
                else:
                    dict_string[row["sous-question"]] = [i]
            else: 
                if row["sous-question"] not in dict_string:
                        dict_string[row["sous-question"]] = []
    f = open("json/"+now.strftime("%Y%m%d%H%M")+"String_search_single.json","w")
    json.dump(dict_string, f)
    print("étape string single")


def string_search_multi(df0, df3):
    now = datetime.now()
    hug_label = [row["HUG_LABEL_FR"].lower() for index, row in df0.iterrows()]

    dict_string = {}    
    for index, row in df3.iterrows():
        strings = [row["string1"], row["string2"], row["string3"], row["string4"], row["string5"], 
                   row["string6"], row["string7"], row["string8"], row["string9"], row["string10"]]
        for i in hug_label:
            for string in strings:
                if str(string).lower() in i:
                    if row["sous-question"] in dict_string:
                        if i not in dict_string[row["sous-question"]]:
                            dict_string[row["sous-question"]].append(i)
                    else:
                        dict_string[row["sous-question"]] = [i]
                else:
                    if row["sous-question"] not in dict_string:
                        dict_string[row["sous-question"]] = []
    f = open("json/"+now.strftime("%Y%m%d%H%M")+"String_search_multi.json","w")
    json.dump(dict_string, f)
    print("étape string multi")


def icd_search(df0, df4):
    now = datetime.now()
    dict_icd = {}
    for index, row in df4.iterrows():
        if isinstance (row["icd"], str): 
            icd_terms = [term.strip() for term in row["icd"].split(",")]
            for icd_term in icd_terms:
                for i, r in df0.iterrows():
                    if icd_term in str(r["ICD10_GM_2023"]):
                        if row["sous-question"] in dict_icd:
                            dict_icd[row["sous-question"]].append(r["HUG_LABEL_FR"])
                        else:
                            dict_icd[row["sous-question"]] = [r["HUG_LABEL_FR"]]
        else:
            dict_icd[row["sous-question"]] = []
    for key in dict_icd:
        dict_icd[key] = list(set(dict_icd[key]))
    f = open("json/"+now.strftime("%Y%m%d%H%M")+"ICD_search.json","w")
    json.dump(dict_icd, f)
    print("étape ICD")






if __name__ == '__main__':

    df0 = pd.read_excel("hug.xlsx")
    xls = pd.ExcelFile("data_ECL_Francois.xlsx")
    df1 = pd.read_excel(xls, 'Questions')
    df2 = pd.read_excel(xls, 'methode1')
    df3 = pd.read_excel(xls, 'methode2')
    df4 = pd.read_excel(xls, "icd")
    df5 = pd.read_excel(xls, "ecl")
    f = open("json/hug_data.json","r")
    hug_data = json.load(f)


    #hugdata()       

    
    snomed(df1, hug_data, df5)


    string_search_single(df0, df2)
    string_search_multi(df0, df3)

    icd_search(df0, df4)



