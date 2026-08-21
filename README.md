LinkedIn Insights Service

A FastAPI-based LinkedIn Insights service that scrapes LinkedIn company
pages, stores the collected data in MongoDB, exposes REST APIs for
querying page insights, and generates AI-powered page summaries using
LangChain and OpenAI.

Features

Scrape LinkedIn company pages using a Page ID / company vanity name

Store page data in MongoDB

Store related people, posts, and comments

Fetch pages from the database

Automatically scrape a page when it is not already stored

Filter pages by follower count, name, and industry

Pagination for page and post queries

Fetch recent posts

Scrape and store comments

Generate AI-powered LinkedIn page summaries using LangChain + OpenAI

Postman collection included

Tech Stack

Python

FastAPI

MongoDB / PyMongo

Pydantic

LangChain

OpenAI

Postman

Project Structure

linkedin-insights-service/
├── app/
│   ├── database/
│   │   └── mongodb.py
│   ├── repository/
│   │   ├── comment_repo.py
│   │   ├── page_repo.py
│   │   ├── person_repo.py
│   │   └── post_repo.py
│   ├── routes/
│   │   └── page_routes.py
│   ├── schemas/
│   │   ├── comment.py
│   │   ├── page.py
│   │   ├── person.py
│   │   └── post.py
│   ├── scraper/
│   │   └── linkedin_scraper.py
│   ├── services/
│   │   ├── aisummary_service.py
│   │   └── page_service.py
│   └── main.py
├── Linkedinapi.postman_collection.json
├── requirements.txt
├── .gitignore
└── test_*.py

How It Works

LinkedIn Page ID
       |
       v
LinkedIn Scraper
       |
       +-- Page details
       +-- People
       +-- Posts
       +-- Comments
       |
       v
     MongoDB
       |
       v
    FastAPI APIs
       |
       +-- Page details
       +-- Filters
       +-- Posts
       +-- AI Summary
                    |
                    v
             LangChain + OpenAI

Page ID

The Page ID is the final part of a LinkedIn company URL.

Example:

https://www.linkedin.com/company/deepsolv/

Page ID:

deepsolv

Requirements

Python 3.10+ recommended

MongoDB

OpenAI API key

Internet access for LinkedIn scraping

Installation

Clone the repository:

git clone https://github.com/guritgb/linkedin-insights-service.git
cd linkedin-insights-service

Create a virtual environment on Windows:

python -m venv venv
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key
MONGO_URI=your_mongodb_connection_string

Do not commit .env or API keys to GitHub.

Run the Application

uvicorn app.main:app --reload

The API runs at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

API Endpoints

Get Page by ID

GET /pages/{page_id}

Example:

GET /pages/deepsolv

If the page exists in MongoDB, the stored data is returned. Otherwise,
the service attempts to scrape the page and store it.

Filter and Paginate Pages

GET /pages

Query parameters:

min_followers

max_followers

name

industry

page

limit

Example:

GET /pages?min_followers=1000&max_followers=100000&name=deep&industry=software%20development&page=1&limit=10

Get Page Posts

GET /pages/{page_id}/posts

Example:

GET /pages/deepsolv/posts?page=1&limit=10

If posts are not stored, the service attempts to scrape posts and their
comments.

Generate AI Summary

GET /pages/{page_id}/aisummary

Example:

GET /pages/deepsolv/aisummary

The AI analyzes available page, follower, employee, post, engagement,
and people data.

Postman

The repository contains:

Linkedinapi.postman_collection.json

Import this file into Postman to test the API.

The collection includes:

Page by ID

Page filtering and pagination

Page posts

AI summary

Database Design

The application separates data into logical entities.

Page

Stores information such as:

Page name

Page URL

LinkedIn ID

Profile picture

Description

Website

Industry

Followers

Headcount

Specialities

Person

Stores people associated with a LinkedIn page.

Post

Stores posts associated with a page and available engagement
information.

Comment

Stores comments associated with posts.

Repository classes keep database operations separate from the API
routes.

AI Summary

The AI service uses LangChain's ChatOpenAI with:

ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

The prompt asks the model to analyze:

Type of page/business

What the page is about

Follower/audience characteristics

Content themes

Likes and comments

High-performing content

Overall insights

The prompt also instructs the model not to invent facts that are not
present in the supplied data.

Testing

The repository contains test scripts for scraping, repositories,
database operations, people, comments, and AI summary generation.

Example:

python testai.py

Notes

LinkedIn's website structure and internal APIs can change over time, so
scraping may require maintenance.

Use the service responsibly and ensure your usage complies with
LinkedIn's applicable terms and policies.

Author

Gurit Bhasin

GitHub: https://github.com/guritgb
