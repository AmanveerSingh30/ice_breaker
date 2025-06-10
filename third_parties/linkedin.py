# filepath: c:\Users\amanv\OneDrive\Desktop\ice_breaker\third_parties\linkedin.py
import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Path to the mock data file
MOCK_DATA_FILE = Path(__file__).parent / "data" / "mock_linkedin_profile.json"


def clean_data(data):
    """Clean the LinkedIn profile data to keep only important information"""
    # Initialize a dictionary to store cleaned data
    cleaned_data = {
        "name": data.get("full_name"),
        "public_identifier": data.get("public_identifier"),
        "profile_pic_url": data.get("profile_pic_url"),
        "headline": data.get("headline"),
        "occupation": data.get("occupation"),
        "location": {
            "country": data.get("country_full_name"),
            "city": data.get("city"),
        },
        "summary": data.get("summary"),
        "experiences": [],
    }

    # Extract relevant experience information
    if data.get("experiences"):
        for experience in data.get("experiences"):
            cleaned_experience = {
                "title": experience.get("title"),
                "company": experience.get("company"),
                "location": experience.get("location"),
                "starts_at": experience.get("starts_at"),
                "ends_at": experience.get("ends_at"),
            }
            cleaned_data["experiences"].append(cleaned_experience)

    # Extract education information
    cleaned_data["education"] = []
    if data.get("education"):
        for education in data.get("education"):
            cleaned_education = {
                "school": education.get("school"),
                "degree_name": education.get("degree_name"),
                "field_of_study": education.get("field_of_study"),
                "starts_at": education.get("starts_at"),
                "ends_at": education.get("ends_at"),
            }
            cleaned_data["education"].append(cleaned_education)

    return cleaned_data


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        # Load mock data from local JSON file
        with open(MOCK_DATA_FILE, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    else:
        # Use the API to get real data
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )
        data = response.json()

    # Extract relevant information from the data
    clean_profile_data = clean_data(data)

    return clean_profile_data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-marco/", mock=True
        ),
    )
