from app.services.aisummary_service import AiSummary


page_data = {
    "page_id": "deepsolv",
    "name": "Deepsolv",
    "industry": "Software Development",
    "followers": 2000,
    "description": "AI Creative Decision Intelligence for growth teams",
    "headcount": "2-10 employees"
}


posts_data = [
    {
        "content": "AI agents are transforming business workflows",
        "likes": 2623,
        "comments": 196
    },
    {
        "content": "How companies are implementing AI",
        "likes": 612,
        "comments": 118
    }
]


people_data = [
    {
        "name": "Vishal V.",
        "profile_url": "https://www.linkedin.com/in/vishal-vishwajeet"
    },
    {
        "name": "Amandeep",
        "profile_url": "https://www.linkedin.com/in/amandeepdtu"
    }
]


service = AiSummary()

summary = service.gen_summary(
    page_data,
    posts_data,
    people_data
)

print("\n========== AI SUMMARY ==========\n")
print(summary)