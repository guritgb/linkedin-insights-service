from app.database.mongodb import db

class CommentRepo:

    def __init__(self):
        self.collection = db["comments"]

    def save_comments(self, comments):
        if not comments:
            return

        for comment in comments:
            self.collection.update_one(
                {"comment_id": comment["comment_id"]},
                {"$set": comment},
                upsert=True
            )

    def getcommentbypost(self,post_id):
        return list(
            self.collection.find(
                {"post_id":post_id},
                {"_id":0}
            )
        )


