from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class AiSummary:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                You are a LinkedIn Page insights analyst.

                Analyze the provided LinkedIn Page data and generate useful,
                concise business insights.

                Do not invent facts that are not present in the data.

                Analyze:
                - What type of page/business this is
                - What the page is about
                - Its follower/audience characteristics based on available data
                - Content themes
                - Engagement based on likes and comments
                - What appears to perform well
                - Overall insights

                Clearly distinguish between facts from the data and reasonable
                inferences.
                """
                            ),
                            (
                                "human",
                                """
                Analyze this LinkedIn Page:

                PAGE DATA:
                {page_data}

                POST DATA:
                {posts_data}

                PEOPLE DATA:
                {people_data}
                """
                    )
        ])


    def gen_summary(self,page_data,posts_data,people_data):
        messages = self.prompt.format_messages(
            page_data=page_data,
            posts_data=posts_data,
            people_data=people_data
        )

        response = self.llm.invoke(messages)
        return response.content