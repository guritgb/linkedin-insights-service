from app.scraper.linkedin_scraper import LinkedinScrapper


scraper = LinkedinScrapper()

page = scraper.scrape_page("deepsolv")

print(page.model_dump())