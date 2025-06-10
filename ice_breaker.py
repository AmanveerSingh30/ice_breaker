import os
from dotenv import load_dotenv
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from third_parties.linkedin import scrape_linkedin_profile


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    print("Hello, world!")

    summary_template = """
    Given the Linkedin information {information} about a person, I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
    )

    chain = summary_prompt_template | llm | StrOutputParser()
    linkedin_data = scrape_linkedin_profile(
        "https://www.linkedin.com/in/eden-marco", mock=True
    )

    res = chain.invoke({"information": linkedin_data})
    print(res)
