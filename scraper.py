
from bs4 import BeautifulSoup
import requests
from tokens import truncate_to_tokens
from config import MAX_PAGE_TOKENS



def fetch_website_links(url):
    """
    Fetches all the links from the given website URL.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        list: A list of all the links found on the website.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [link['href'] for link in soup.find_all('a', href=True)]
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []


def fetch_website_content(url):
    """
    Fetches the content of the given website URL.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The content of the website, truncated to MAX_PAGE_TOKENS tokens.
    """

    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser') 
        title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""

        return truncate_to_tokens(title + "\n\n" + text, MAX_PAGE_TOKENS)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""


