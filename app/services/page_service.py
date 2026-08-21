from app.repository.page_repo import PageRepo
from app.schemas.page import Page

class PageService:

    def __init__(self):
        self.repository = PageRepo()

    def savepage(self, page:Page):
        return self.repository.upsert(page)

    def getpage(self, page_id:str):
        return self.repository.getbypageid(page_id)

    