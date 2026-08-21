from app.database.mongodb import db
from app.schemas.person import Person

class PersonRepo:

    def __init__(self):
        self.collection = db.people

    def upsert(self, person:Person):
        res = self.collection.update_one(
            {"person_id":person.person_id,
             "page_id": person.page_id},
            {"$set":person.model_dump()},
            upsert = True
        )

        return res

    def getby_pageid(self,page_id:str):
        return list(
            self.collection.find(
                {"page_id":page_id},
                {"_id":0}
            )
        )

    