# Sales Brochure Generator

Generate a short Markdown company brochure for prospective customers, investors, and recruits using content from the company's public website.

The project scrapes the landing page and its links, asks an OpenAI model to select relevant pages, then uses their content to write the brochure.

## Requirements

- Python 3
- An OpenAI API key with access to the model you configure
- Network access to the target website and OpenAI API

## Setup

Create and activate a virtual environment, then install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```dotenv
OPENAI_API_KEY=your-openai-api-key
API_Model=gpt-4o-mini
```

`API_Model` is the model name used for link selection and brochure generation. Set it to a model available to your OpenAI account.

## Generate a brochure

The module exposes `create_brochure(website_url)` to print a complete brochure and `stream_brochure(website_url)` to print generated content as it arrives. Call either function from the project directory:

```bash
python -c 'from brochure_generation import create_brochure; create_brochure("https://example.com")'
```

For streamed output:

```bash
python -c 'from brochure_generation import stream_brochure; stream_brochure("https://example.com")'
```

Replace `https://example.com` with the company's website URL. The brochure is printed to the terminal in Markdown; it is not saved to a file.

## Current limitations

- The scraper reads HTML pages and extracts visible page text; it does not execute JavaScript.
- Each fetched page is limited to 2,000 characters, and the brochure prompt is limited to 5,000 characters.
- Website requests can fail because of network errors or site restrictions.
