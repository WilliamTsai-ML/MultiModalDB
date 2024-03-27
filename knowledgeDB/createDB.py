import os
from pathlib import Path
from PIL import Image
from knowledgeDB.dbAPI import DBobject
from knowledgeDB.encoderAPI import blipAPI, llmAPI


def run():
    print("Creating DB")

    db = DBobject()
    llm = llmAPI()
    blip = blipAPI()
    db.set_language_model(llm)
    db.set_blip_model(blip)
    
    docs = []
    file_names = []
    for file in os.listdir("./docs"):
        if file.endswith(".txt"):
            with open(f"./docs/{file}", "r") as f:
                docs.append(f.read())
                file_names.append(Path(file))
        if file.endswith(".jpg"):
            docs.append(Image.open(f"./docs/{file}"))
            file_names.append(Path(file))
        print(f"Processed {file}")
    
    db.add(ids=[f"{file_names[i].stem}" for i in range(len(docs))], docs=docs)
        