import re
import requests
import json
import hashlib
from bs4 import BeautifulSoup
from app.schemas.page import Page
from playwright.sync_api import sync_playwright

class  LinkedinScrapper:
    def __init__(self):
        self.headers ={
            "User-Agent":"Mozilla/5.0"
        }

    def scrape_page(self , page_id:str)->Page:
        url = f"https://www.linkedin.com/company/{page_id}/"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        name = self.extract_name(soup)
        description = self.extract_description(soup)
        website = self.extract_website(soup)
        industry= self.extract_aboutfield(soup,"about-us__industry")
        headcount = self.extract_aboutfield(soup,"about-us__size")
        followers = self.extract_followers(soup)
        profile_pic = self.extract_profilepicture(soup)

        return Page(
            page_id=page_id,
            linkedin_id=None,
            name=name,
            url=url,
            profile_pic=profile_pic,
            description=description,
            website=website,
            industry=industry,
            followers=followers,
            headcount=headcount,
            specialities=[]
        )

    def extract_name(self,soup):
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        return None

    def extract_aboutfield(self,soup,field_name):
        element =soup.find(
            attrs={"data-test-id":field_name}
        )
        if not element:
            return None

        dd= element.find("dd")
        if dd:
            return dd.get_text(" ",strip=True)

        return None

    def extract_followers(self,soup):
        meta = soup.find(
            "meta",
            attrs = {"name":"description"}
        )
        if not meta:
            return None

        description = meta.get("content","")

        match = re.search(
            r"([\d,]+)\s+followers",
            description,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1).replace(",", ""))

        return None

    def extract_profilepicture(self, soup):
        meta = soup.find(
            "meta",
            attrs={"name": "twitter:image"}
        )

        if meta:
            return meta.get("content")

        return None

    def extract_description(self, soup):
        element = soup.find(
            attrs={"data-test-id": "about-us__description"}
        )

        if element:
            return element.get_text(" ", strip=True)

        return None

    def extract_website(self, soup):
        element = soup.find(
            attrs={"data-test-id": "about-us__website"}
        )

        if not element:
            return None

        link = element.find("a")

        if link:
            return link.get("href")

        return None

    def parse_count(self, value):
        if not value:
            return 0

        value = value.strip().upper().replace(",", "")

        try:
            if value.endswith("K"):
                return int(float(value[:-1]) * 1000)

            if value.endswith("M"):
                return int(float(value[:-1]) * 1000000)

            return int(value)

        except ValueError:
            return 0
    def scarpe_post(self,soup,page_id):
        posts = soup.find_all(
            "article",
            attrs={"data-id":"main-feed-card"}
        )

        results=[]

        for post in posts[:15]:
            activityurl = post.get("data-activity-urn")

            if not activityurl:
                continue

            post_id = activityurl.split(":")[-1]

            content_ele = post.find(
                "p",
                attrs={"data-test-id":"main-feed-activity-card__commentary"}
            )

            content =(
                content_ele.get_text(" ",strip=True)
                if content_ele
                else None
            )

            reaction = post.find(
                "span",
                attrs={"data-test-id":"social-actions__reaction-count"}
            )

            likes = (
                self.parse_count(reaction.get_text(strip=True))
                if reaction
                else 0
            )

            comment_ele = post.find(
                "a",
                attrs={"data-test-id":"social-actions__comments"}
            )

            commentcount =(
                int(comment_ele.get("data-num-comments",0))
                if comment_ele
                else 0
            )

            time_ele = post.find("time")
            posted_at =(
                time_ele.get_text(" ",strip=True)
                if time_ele
                else None
            )

            results.append({
                "post_id":post_id,
                "page_id": page_id,
                "content":content,
                "likes":likes,
                "posted_at":posted_at,
                "comments_count":commentcount
            })

        return results

    def scrape_posts(self, page_id: str):
        url = f"https://www.linkedin.com/company/{page_id}/"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        return self.scarpe_post(soup, page_id)

    def scrape_comments(self, post_id):
        url = f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=15
        )

        response.raise_for_status()
        

        soup = BeautifulSoup(response.text, "html.parser")

        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        for script in scripts:
            try:
                data = json.loads(script.string)

                if "comment" in data:
                    comments = data["comment"]

                    print(f"JSON-LD comments found: {len(comments)}")

                    scraped_comments = []

                    for comment in comments:

                        author = comment.get(
                            "author", {}
                        ).get("name")

                        content = comment.get("text")

                        posted_at = comment.get("datePublished")

                        comment_id = hashlib.sha256(
                            f"{post_id}|{author}|{posted_at}|{content}".encode("utf-8")
                        ).hexdigest()

                        scraped_comments.append({
                            "comment_id": comment_id,
                            "post_id": post_id,
                            "author": author,
                            "content": content,
                            "posted_at": posted_at,
                            "likes": comment.get(
                                "interactionStatistic",
                                {}
                            ).get(
                                "userInteractionCount",
                                0
                            )
                        })

                    return scraped_comments

            except (json.JSONDecodeError, TypeError):
                continue
        comment_elements = soup.find_all(
            attrs={
                "data-test-id": "comment"
            }
        )

        print(f"DOM comments found: {len(comment_elements)}")

        scraped_comments = []

        for comment in comment_elements:
            print(comment.get_text(" ", strip=True))

        return scraped_comments

    # def scrape_people(self , page_id:str):
    #     url = f"https://www.linkedin.com/company/{page_id}/people/"

    #     response = requests.get(
    #         url,headers=self.headers,timeout=15
    #     )

    #     response.raise_for_status()
    #     soup = BeautifulSoup(response.text,"html.parser")
    #     people=[]

    #     gg = soup.find_all(
    #         "li",
    #         check=re.compile("org-people-profile-card")
    #     )
    #     print(len(gg))
    #     for g in gg:
    #         print(g.get_text(" ",strip=True))

    #     return people

    def scrape_people(self, page_id: str):

        url = f"https://www.linkedin.com/company/{page_id}/people/"

        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                "linkedin_profile",
                headless=False
            )
            page = context.pages[0] if context.pages else context.new_page()

            page.goto( url,wait_until="domcontentloaded")

            print("People page:", page.url)
            print("Title:", page.title())
            page.wait_for_timeout(5000)

            input("Press ENTER after checking the People page...")

            links = page.locator('a[href*="/in/"]')

            print("PROFILE LINKS:", links.count())
            people = {}

            for i in range(links.count()):
                link = links.nth(i)
                href = link.get_attribute("href")
                text = link.inner_text().strip()

                if not href:
                    continue

                profile_url = href.split("?")[0]
                username = profile_url.rstrip("/").split("/")[-1]

                if username.startswith("ACo"):
                    continue

                if not text:
                    continue

                excluded_text = [
                    "follows this page",
                    "school alum",
                    "contact us",
                    "provides services"
                ]

                if any(
                    value in text.lower()
                    for value in excluded_text
                ):
                    continue

                if username not in people:

                    people[username] = {
                        "person_id": username,
                        "page_id": page_id,
                        "name": text,
                        "profile_url": profile_url
                    }

            context.close()

            return list(people.values())