import sys
from knowledgeDB.dbAPI import DBobject
from knowledgeDB.encoderAPI import blipAPI, llmAPI


def run():

    db = DBobject()
    llm = llmAPI()
    blip = blipAPI()
    db.set_language_model(llm)
    db.set_blip_model(blip)

    search_query = sys.argv[1]
    text_results, image_results = db.query(search_query)
    print(f"Searching for matching results about {sys.argv[1]}")
    print("Top document results:")
    for res in text_results:
        print(res)
    print("Top image results:")
    for res in image_results:
        print(res)

