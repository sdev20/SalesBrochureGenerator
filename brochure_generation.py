import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from prompts import get_brochure_system_prompt, get_brochure_user_prompt, get_relevant_links_system_prompt, get_relevant_links_user_prompt
from scraper import fetch_website_content, fetch_website_links



load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
else:
    print("OPENAI_API_KEY environment variable is set.")

openAI = OpenAI()
model = os.getenv("API_Model")

def fetch_relevant_links(links, website_url):
    """
    Fetches relevant links for brochure generation from the given list of links.

    Args:
        links (list): The list of links to process.
        website_url (str): The URL of the website to scrape.
    """

    response = OpenAI().chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": get_relevant_links_system_prompt()},
            {"role": "user", "content": get_relevant_links_user_prompt(links, website_url)}
        ],
        response_format={"type": "json_object"} # Specify the response format as JSON
    )

    relevant_links = response.choices[0].message.content
    return json.loads(relevant_links)  # Parse the JSON string into a Python dictionary

def fetch_content_and_relevant_links(website_url):
    """
    Fetches the content of the given website URL and relevant links for brochure generation.

    Args:
        links (list): The list of links to process.
        website_url (str): The URL of the website to scrape.
    """

    # fetch the list of links from the website
    links = fetch_website_links(website_url) 

    # fetch the content of the website
    content = fetch_website_content(website_url)

    # fetch the relevant links for brochure generation
    relevant_links = fetch_relevant_links(links, website_url)

    # format the content and relevant links for brochure generation
    result = f"## Landing Page:\n\n{content}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_content(link["url"])
    return result


def create_brochure(website_url):
    """
    Creates a brochure for the given website URL.

    Args:
        website_url (str): The URL of the website to scrape.
    """
    company_content = fetch_content_and_relevant_links(website_url)
    brochure_response = openAI.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": get_brochure_system_prompt()},
                {"role": "user", "content": get_brochure_user_prompt(company_content)}
            ],
        )

    result = brochure_response.choices[0].message.content
    print(result)


def stream_brochure(website_url):
    """
    Creates a brochure for the given website URL.

    Args:
        website_url (str): The URL of the website to scrape.
    """
    company_content = fetch_content_and_relevant_links(website_url)
    brochure_response = openAI.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": get_brochure_system_prompt()},
                    {"role": "user", "content": get_brochure_user_prompt(company_content)}
                ],
                stream=True
            )

    result = ""
    for chunk in brochure_response:
        if chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content
            print(result)



