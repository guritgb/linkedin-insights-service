from fastapi import APIRouter , HTTPException ,Query
from app.database.mongodb import db
from typing import Optional
from app.schemas.person import Person
from app.services.page_service import PageService
from app.repository.page_repo import PageRepo
from app.repository.comment_repo import CommentRepo
from app.services.aisummary_service import AiSummary
from app.repository.post_repo import PostRepo
from app.repository.person_repo import PersonRepo
from app.scraper.linkedin_scraper import LinkedinScrapper

page_router = APIRouter(prefix="/pages",tags=["Pages"])
service = PageService()
pagerepo = PageRepo()
postrepo = PostRepo(db)
personrepo = PersonRepo()
commentrepo = CommentRepo()
scraper = LinkedinScrapper()
aiwork = AiSummary()

# @page_router.get("/{page_id}")
# def get_page(page_id:str):
#     page = service.getpage(page_id)

#     if not page:
#         raise HTTPException(
#             status_code=404,
#             detail="page not found"
#         )

#     page["_id"] = str(page["_id"])
#     return page

@page_router.get("/{page_id}")
def get_pages(page_id:str):
    page = pagerepo.getbypageid(page_id)

    if page:
        page.pop("_id",None)
        return page

    try:
        scrape_page = scraper.scrape_page(page_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to scrap page: {page_id}"
        )

    pagerepo.upsert(scrape_page)

    try:
        people = scraper.scrape_people(page_id)

        for person in people:
            person = Person(**person)
            personrepo.upsert(person)

    except Exception as e:
        print(f"failed to scrape people for {page_id}:{e}")

    
    return scrape_page.model_dump()

@page_router.get("")
def get_pages_new(
    min_followers:Optional[int]=Query(None),
    max_followers:Optional[int]=Query(None),
    name:Optional[str] = Query(None),
    industry:Optional[str]= Query(None),
    page:int = Query(1,ge=1),
    limit:int = Query(10,ge=1,le=100)
    ):
    return pagerepo.getpages(
        min_followers=min_followers,
        max_followers=max_followers,
        name=name,
        industry=industry,
        page=page,
        limit=limit
    )

@page_router.get("/{page_id}/posts")
def get_page_posts(page_id:str,page:int=1,limit:int=10):
    skip = (page-1)*limit

    posts = postrepo.getpostbypage(page_id,skip,limit)

    if not posts:
        try:
            scraped_postd = scraper.scrape_posts(page_id)

            if scraped_postd:
                postrepo.save_posts(scraped_postd)

                for post in scraped_postd:
                    comments = scraper.scrape_comments(post["post_id"])

                    if comments:
                        commentrepo.save_comments(comments)

                posts = postrepo.getpostbypage(page_id,skip,limit)

        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"failed to scrape posts for this {page_id}"
            )

    for post in posts:
        post["_id"] = str(post["_id"])

    return posts


@page_router.get("/{page_id}/aisummary")
def get_ai_summary(page_id:str):
    page = pagerepo.getbypageid(page_id)

    if not page:
        raise HTTPException(
        status_code=404,
        detail="page not found"
        )

    page.pop("_id",None)

    posts = postrepo.getpostbypage(page_id,skip=0,limit=10)
    for post in posts:
        post.pop("_id",None)


    people =[]

    try:
        people = personrepo.getby_pageid(page_id)

        for person in people:
            person.pop("_id",None)

    except Exception as e:
        print(f"Failed to get people:{e}")

    try:

        summary = aiwork.gen_summary(page,posts,people)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"failed to generate summary: {str(e)}"
        )

    return {
        "page_id":page_id,
        "summary":summary
    }