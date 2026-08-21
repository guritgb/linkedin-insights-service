from app.scraper.linkedin_scraper import LinkedinScrapper


scraper = LinkedinScrapper()

people = scraper.scrape_people("deepsolv")

print("\n========== PEOPLE ==========")

for person in people:
    print(person)

print("\nTOTAL:", len(people))