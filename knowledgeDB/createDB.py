from knowledgeDB.dbAPI import DBobject
from knowledgeDB.llmAPI import llmAPI


def run():
    print(f"[{__file__} Hello World")

    db = DBobject()
    llm = llmAPI()
    db.set_language_model(llm)
    