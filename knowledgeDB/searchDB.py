import sys
from knowledgeDB.dbAPI import DBobject
from knowledgeDB.llmAPI import llmAPI


def run():
    print(f"[{__file__} Hello World")

    db = DBobject()
    llm = llmAPI()
    db.set_language_model(llm)

    search_query = sys.argv[1]
    print(db.query(search_query))

