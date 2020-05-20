
import lzma
import json
from elasticsearch import Elasticsearch
import logging


case_index_name = "cases"
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index=case_index_name, ignore=400)


def get_case_law_data():
    with lzma.open("data/mexico.jsonl.xz") as in_file:
        for line in in_file:
            case = json.loads(str(line, 'utf8'))
            print(case['name'])
            print(case.keys())
            print(case["casebody"]["data"]["head_matter"])
            # opinons has the bulk of the actual text
            # print(case["casebody"]["data"].keys())
            print(case['decision_date'])
            break


def create_case_index(case_file_path):
    i = 0
    max_docs = 1000
    with lzma.open(case_file_path) as in_file:
        for line in in_file:
            i += 1
            case = json.loads(str(line, 'utf8'))
            # print(case['name'])
            # print(case.keys())
            # print(case["casebody"]["data"]["head_matter"])
            # # opinons has the bulk of the actual text
            # # print(case["casebody"]["data"].keys())
            # print(case['decision_date'])

            index_status = es.index(index=case_index_name, id=i, body=case)
            print(index_status)

            if (i == max_docs):
                break


def run_query(search_query):
    search_query = {
        "_source": ["name"],
        "query": {
            "multi_match": {
                "query":    "imprisonment",
                "fields": ["casebody.data.opinions.text", "name"]
            }
        },
        "size": 3
    }
    query_result = es.search(index=case_index_name, body=search_query)
    # print(len(query_result["hits"]["hits"]), " hits ..")
    print((query_result), " hits ..")
    return query_result


# case_file_path = "data/mexico.jsonl.xz"
# create_case_index(case_file_path)