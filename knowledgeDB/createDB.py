import os
from pathlib import Path
from knowledgeDB.dbAPI import DBobject
from knowledgeDB.llmAPI import llmAPI


def run():
    print("Creating DB")

    db = DBobject()
    llm = llmAPI()
    db.set_language_model(llm)
    
    docs = []
    file_names = []
    for file in os.listdir("./docs"):
        with open(f"./docs/{file}", "r") as f:
            docs.append(f.read())
            file_names.append(Path(file))
        print(f"Processed {file}")
    
    db.add(ids=[f"{file_names[i].stem}" for i in range(len(docs))], docs=docs)
        