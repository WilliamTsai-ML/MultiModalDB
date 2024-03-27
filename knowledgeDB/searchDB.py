import sys
from knowledgeDB.dbAPI import DBobject
from knowledgeDB.llmAPI import llmAPI


def run():
    print(f"Searching for matching news articles about {sys.argv[1]}")

    db = DBobject()
    llm = llmAPI()
    db.set_language_model(llm)

    search_query = sys.argv[1]
    print("Top results:")
    for res in db.query(search_query):
        print(res)

