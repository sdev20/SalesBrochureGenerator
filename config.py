import os
from dotenv import load_dotenv

load_dotenv()

MAX_LINKS_PER_PAGE = 10

# Maximum number of tokens kept per page. A token cap is used instead of a character cap because
# tokens per character vary a lot between pages (e.g. pricing pages cost ~4x more than prose).
MAX_PAGE_TOKENS = 2_500

# Maximum tokens of scraped content sent in one brochure request (prompts and output excluded).
# This is a guard for cost and quality, not the context-window limit.
MAX_CONTENT_TOKENS = 25_000

API_MODEL = "gpt-4o-mini"

CHUNK_TOKENS_SIZE = 350

CHUNK_OVERLAP_TOKENS_SIZE = 50

# Switches the pipeline to the RAG path: pages are fetched without the per-page token cap
# so they can be chunked and ranked. Set RAG_ENABLED=true in .env to turn it on; off by default.
RAG_ENABLED = os.getenv("RAG_ENABLED", "false").strip().lower() in ("1", "true", "yes")

EMBEDDING_MODEL="text-embedding-3-small"

EMBEDDING_BATCH_SIZE=100
