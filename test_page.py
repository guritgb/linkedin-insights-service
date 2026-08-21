from app.database.mongodb import db
from app.schemas.page import Page

page = Page(
    page_id="deepsolv",
    linkedin_id="12345",
    name="Deepsolv",
    url="https://www.linkedin.com/company/deepsolv/",
    followers=25000,
    headcount=50,
    description="blah blah blah",
    industry="Tech",
    specialities=["AI","SDE"]
)

db.pages.create_index("page_id", unique=True)
res = db.pages.insert_one(page.model_dump())
print(res.inserted_id)
