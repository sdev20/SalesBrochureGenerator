from config import EMBEDDING_BATCH_SIZE, EMBEDDING_MODEL
from tokens import tokens_to_text, text_to_tokens
from llm_client import client
import numpy as np


def chunk_text(text, chunk_token_size, overlap_token_size):
    """
    Chunks the given text into smaller pieces based on the specified token size and overlap size.
    Chunk based on tokens rather than characters as tokens per character vary a lot between pages and using characters may lead to inconsistent chunk sizes.

    Args:
        text (str): The text to be chunked.
        chunk_token_size (int): The maximum number of tokens per chunk.
        overlap_token_size (int): The number of overlapping tokens between consecutive chunks.

    Returns:
        list: A list of text chunks.
    """

    if overlap_token_size >= chunk_token_size:
        raise ValueError("Overlap size must be smaller than chunk size.")

    text_tokens = text_to_tokens(text)
    start = 0

    chunks = []
    len_tokens = len(text_tokens)

    while start < len_tokens:
        # Determine the end index for the current chunk based on the chunk size.
        end = start + chunk_token_size
        tokens = text_tokens[start:end]
        chunk = tokens_to_text(tokens)
        chunks.append(chunk)

        # Move the start index forward by the chunk size minus the overlap size to get overlapping content from the previous chunk.
        start += chunk_token_size - overlap_token_size

        # If the remaining tokens are less than or equal to the overlap size ( which means it is only overlapping content from the previous chunk), 
        # stop creating new chunks.
        if len_tokens - start <= overlap_token_size:
            break
    return chunks


def chunk_pages(pages, chunk_token_size, overlap_token_size):
    """
    Chunks the content of multiple pages into smaller pieces based on the specified token size and overlap size.

    Args:
        pages (list): A list of dictionaries, each containing "url", "type", and "content" keys.
        chunk_token_size (int): The maximum number of tokens per chunk.
        overlap_token_size (int): The number of overlapping tokens between consecutive chunks.

    Returns:
        list: A list of dictionaries, each containing "url", "type", "chunk content", and "index" keys for each chunk.
    """
    all_chunks = []
    for page in pages:
        chunks_of_page = chunk_text(page["content"], chunk_token_size, overlap_token_size)
        for i, chunk_of_page in enumerate(chunks_of_page):
            chunk = {"url": page["url"], "type": page["type"], "content": chunk_of_page, "index": i}
            all_chunks.append(chunk)

    return all_chunks


def embed_texts(texts):
    start = 0
    vectors = []
    while start < len(texts):
        batch = texts[start:start + EMBEDDING_BATCH_SIZE]

        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        vectors.extend([item.embedding for item in response.data])
        start += EMBEDDING_BATCH_SIZE

    return np.array(vectors, dtype = np.float32)
