from app.repository.page_repo import PageRepo
from app.schemas.page import Page

repo = PageRepo()

page = Page(
    page_id="test",
    linkedin_id="123456",
    name="company",
    url="https://www.linkedin.com/company/testcompany/",
    followers=1000,
    headcount=20,
    description="description",
    industry="Tech",
    specialities=["SDE"]
)

res = repo.upsert(page)
print(res)

foundpage = repo.getbypageid("test")
print(foundpage)