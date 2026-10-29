
MAX_LINKS_PER_PAGE = 10

# Maximum number of tokens kept per page. A token cap is used instead of a character cap because
# tokens per character vary a lot between pages (e.g. pricing pages cost ~4x more than prose).
MAX_PAGE_TOKENS = 2_500

# Maximum tokens of scraped content sent in one brochure request (prompts and output excluded).
# This is a guard for cost and quality, not the context-window limit.
MAX_CONTENT_TOKENS = 25_000


API_MODEL = "gpt-4o-mini"
