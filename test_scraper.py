import requests
from bs4 import BeautifulSoup
from app.scraper.linkedin_scraper import LinkedinScrapper
# from app.scraper.linkedin_scraper import scarpe_post
from app.repository.comment_repo import CommentRepo
from app.repository.page_repo import PageRepo
from app.repository.post_repo import PostRepo
from app.database.mongodb import db
url = "https://www.linkedin.com/company/deepsolv/"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("Status:", response.status_code)
print("Length:", len(response.text))
# print(response.text[:500])

soup = BeautifulSoup(response.text , "html.parser")
print("Title: ", soup.title.text if soup.title else "No title")

print("\n H1: ")
h1 = soup.find("h1")

if h1:
    print(h1.get_text(strip=True))
else:
    print("not found")


print("\nMeta tags:")

for meta in soup.find_all("meta"):
    name = meta.get("name")
    content = meta.get("content")

    if name and content:
        print(name,"=>",content)


print("\nSCRIPT TAG SEARCH:")

html = response.text

keywords = [
    "companyId",
    "staffCount",
    "employeeCount",
    "industry",
    "followerCount",
]

for keyword in keywords:
    print(f"\n--- {keyword} ---")

    position = html.find(keyword)

    if position != -1:
        print(html[position - 200:position + 500])
    else:
        print("Not found")

print("\nABOUT SECTION:")

about_elements = soup.find_all(
    attrs={"data-test-id": lambda value: value and "about-us__" in value}
)

for element in about_elements:
    print(
        element.get("data-test-id"),
        "=>",
        element.get_text(" ", strip=True)
    )

print("\nEXTRACTED DATA:")

# Name
h1 = soup.find("h1")
name = h1.get_text(strip=True) if h1 else None

print("Name:", name)


# Industry
industry_element = soup.find(
    "div",
    {"data-test-id": "about-us__industry"}
)

industry = None

if industry_element:
    dd = industry_element.find("dd")
    if dd:
        industry = dd.get_text(strip=True)

print("Industry:", industry)

description_element = soup.find(
    attrs={"data-test-id": "about-us__description"}
)

print("\nDESCRIPTION HTML:")
print(description_element.prettify() if description_element else "Not found")

print("\nPOST SEARCH:")

keywords = [
    "posts",
    "activity",
    "likes",
    "comments"
]

for keyword in keywords:
    print(f"\n--- {keyword} ---")

    position = response.text.lower().find(keyword.lower())

    if position != -1:
        print(response.text[position - 300:position + 700])
    else:
        print("Not found")


print("\nNUMBER OF POSTS:")

posts = soup.find_all(
    "article",
    attrs={"data-id": "main-feed-card"}
)

print(len(posts))
if posts:
    print("\nFIRST POST:")
    print(posts[0].prettify()[:5000])


print("\nFIRST POST TEXT:")

print(posts[0].get_text(" ", strip=True))


social_bar = posts[0].find(
    "div",
    class_=lambda value: value and "social-action-bar" in value
)

print("\nSOCIAL BAR:")

if social_bar:
    print(social_bar.prettify()[-5000:])
else:
    print("Not found")

print("\nELEMENT CONTAINING 117:")

like_text = posts[0].find(string=lambda text: text and "117" in text)

if like_text:
    print(like_text.parent.prettify())
else:
    print("Not found")


print("\nCONTENT ELEMENT:")

content_element = posts[0].find(
    string=lambda text: text and "Almost a year ago" in text
)

if content_element:
    print(content_element.parent.prettify()[:3000])
else:
    print("Not found")

print("\n")

scraper = LinkedinScrapper()
scraped_posts = scraper.scarpe_post(soup, "deepsolv")
post_repo = PostRepo(db)
# post_repo.save_posts(scraped_posts)

print("posts saved: ", len(scraped_posts))

# print("\nCOMMENT ELEMENT SEARCH:")

# comment_keywords = [
#     "comment",
#     "comments",
#     "commentary"
# ]

# for keyword in comment_keywords:
#     print(f"\n--- {keyword} ---")

#     position = str(posts[0]).lower().find(keyword.lower())

#     if position != -1:
#         print(str(posts[0])[position - 500:position + 1500])
#     else:
#         print("Not found")

print("\nbing")


# comment_repo = CommentRepo()

# all_comments = []

# for post in scraped_posts:
#     post_id = post["post_id"]
#     print(f"\nScraping comments for post: {post_id}")
#     comments = scraper.scrape_comments(post_id)
#     print(f"Comments found: {len(comments)}")
#     all_comments.extend(comments)

# print(f"\ntotal:{len(all_comments)}")

# comment_repo.save_comments(all_comments)


print("\n")
# page = scraper.scrape_page("deepsolv")

# page_repo = PageRepo()
# result = page_repo.upsert(page)

print("PAGE SAVED")

people = scraper.scrape_people("deepsolv")
print(people)