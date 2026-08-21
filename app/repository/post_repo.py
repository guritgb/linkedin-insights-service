from app.database.mongodb import db

class PostRepo:

    def __init__(self,db):
        self.collection  = db.posts

        self.collection.create_index(
            "post_id",
            unique=True
        )

    def save_posts(self,posts):
        if not posts:
            return

        for post in posts:
            self.collection.update_one(
                {"post_id":post["post_id"]},
                {"$set":post},
                upsert=True
            )

    def getpostbypage(self,page_id:str,skip:int=0,limit:int=10):
        return list(
            self.collection.find(
                {"page_id":page_id}
            ).sort("_id",-1).skip(skip).limit(limit)
        )