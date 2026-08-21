from app.database.mongodb import db
from app.schemas.page import Page

class PageRepo:

    def __init__(self):
        self.collection = db.pages

    # def create(self, page:Page):
    #     res = self.collection.insert_one(page.model_dump())
    #     return res.inserted_id

    def upsert(self,page:Page):
        res = self.collection.update_one(
            {"page_id":page.page_id},
            {"$set": page.model_dump()},
            upsert=True
        )
        return res

    def getbypageid(self, page_id:str):
        return self.collection.find_one(
            {"page_id":page_id}
        )

    def getpages(
            self,min_followers=None,max_followers=None,name=None,industry=None,page=1,limit=10
    ):

        query={}
        if min_followers is not None or max_followers is not None:
            query["followers"]={}

            if min_followers is not None:
                query["followers"]["$gte"]= min_followers

            if max_followers is not None:
                query["followers"]["$lte"] = max_followers

        if name:
            query["name"]={
                "$regex":name,
                "$options":"i"
            }

        if industry:
            query["industry"]={
                "$regex":industry,
                "$options":"i"
            }

        skip = (page-1)*limit
        pages= list(
            self.collection.find(query,{"_id":0}).skip(skip).limit(limit)
        )

        total = self.collection.count_documents(query)

        return{
            "total":total,
            "page":page,
            "limit":limit,
            "pages":pages
        }

