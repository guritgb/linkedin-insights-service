from app.scraper.linkedin_scraper import LinkedinScrapper
from app.repository.person_repo import PersonRepo
from app.schemas.person import Person


acraper = LinkedinScrapper()
repo = PersonRepo()
people = acraper.scrape_people("deepsolv")

for data in people:
    person = Person(**data)
    repo.upsert(person)

print(f"saved {len(people)} people")