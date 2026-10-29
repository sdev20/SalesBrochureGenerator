# Sales Brochure Generator

Generate a short Markdown company brochure for prospective customers, investors, and recruits using content from the company's public website.

## How it works

1. `scraper.py` fetches the landing page and collects every link on it.
2. An OpenAI model picks the links that matter for a brochure (about, products, careers, and so on) and returns them as JSON.
3. Each selected page is fetched, cleaned to visible text, and cut to a per-page token limit.
4. The pages are joined into one prompt, and the model writes the brochure.

## Project layout

| File | Purpose |
|---|---|
| `main.py` | Command-line entry point |
| `brochure_generation.py` | Pipeline: link selection, page fetching, brochure generation (normal and streaming) |
| `scraper.py` | Fetches links and page text with `requests` and BeautifulSoup |
| `tokens.py` | Token counting and truncation with `tiktoken` |
| `prompts.py` | System and user prompts |
| `config.py` | Model name and size limits |

## Requirements

- Python 3
- An OpenAI API key with access to the configured model
- Network access to the target website and the OpenAI API

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a `.env` file in the project directory with your API key:

```dotenv
OPENAI_API_KEY=your-openai-api-key
```

The model name and size limits are set in `config.py`, not in `.env`.

## Generate a brochure

```bash
python main.py https://example.com
```

The brochure is printed to the terminal in Markdown; it is not saved to a file. To stream output as it is generated, add --stream argument in command

## Configuration (`config.py`)

| Setting | Value | Meaning |
|---|---|---|
| `API_MODEL` | `gpt-4o-mini` | Model used for link selection and brochure generation |
| `MAX_LINKS_PER_PAGE` | 10 | Maximum linked pages fetched in addition to the landing page |
| `MAX_PAGE_TOKENS` | 2,500 | Tokens kept per page |
| `MAX_CONTENT_TOKENS` | 25,000 | Planned limit for all scraped content in one request (not enforced yet) |

## Design decisions

**Why limit scraped content at all?** The model's context window is large (200k tokens for the model I checked), so the limits are not about fitting. They keep cost and latency down, stop noisy text from diluting the useful facts, and protect against unusually large pages or link lists.

**Why a token limit and not a character limit?** Tokens per character vary a lot between pages. On huggingface.com, the pricing and enterprise pages hit the old 8,000-character cap but cost 7,240 and 6,362 tokens, while ordinary pages cost about 1,500. Those two pages alone were about 57% of the input. A token cap controls what the model actually reads and what is billed.

**Why `tiktoken`?** It counts tokens the way OpenAI models do, so limits can be set in the unit that matters.

**Why 2,500 tokens per page?** Most pages measured between 250 and 2,000 tokens, so 2,500 leaves them whole and only trims outliers. It also roughly matches the average share of the content budget: 25,000 tokens across 11 pages is about 2,270.


## Current limitations

- The scraper reads HTML and does not run JavaScript, so script-rendered sites return little text (google.com's landing page is about 33 tokens). With thin input, the model may fill gaps from what it already knows, so check the brochure against the source.
- The total content limit (`MAX_CONTENT_TOKENS`) is not enforced yet. Eleven pages at 2,500 tokens can reach 27,500.
- The link-selection step can return near-duplicate pages (for example several news articles).
- Navigation, footer, and similar boilerplate text is not removed from pages.
- Website requests can fail because of network errors or site restrictions, and there is no request timeout yet.
