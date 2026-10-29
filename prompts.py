def get_relevant_links_system_prompt():
    return """
You are a helpful assistant that extracts relevant links from a list of links found on a website for company brochure generation. 
Please provide only the relevant links in a JSON format as this example. See if you can make relative URLs to absolute URLs based on the website URL.
{
    "links": [
        {"type": "product", "url": "https://www.example.com/product1"},
        {"type": "about", "url": "https://www.example.com/about"},
        {"type": "contact", "url": "https://www.example.com/contact"},
        {"type": "technology", "url": "https://www.example.com/technology"},
        {"type": "careers", "url": "https://www.example.com/careers"},
    ]
}
"""

def get_relevant_links_user_prompt(links, website_url):
    return f"""You are given a list of links {links} for the website {website_url}.
Please decide which of these are relevant links for company brochure generation.
Do not include Terms of Service, Privacy Policy, or any other irrelevant links.
"""



def get_brochure_system_prompt():
    return """You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information."""


def get_brochure_user_prompt(content):
    user_prompt = f"""
You are looking at a company.
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += f"{content}"
    return user_prompt