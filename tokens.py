import tiktoken
from config import API_MODEL


model = API_MODEL
try:
    encoding = tiktoken.encoding_for_model(model)
except KeyError:
    print(f"Encoding for model {model} not found. Initializing with default encoding.")  
    encoding = tiktoken.get_encoding("o200k_base")

def get_tokens_count(text):
    return len(text_to_tokens(text))

def get_truncated_text(text, max_tokens):
    tokens = encoding.encode(text)
    tokens = tokens[:max_tokens]
    return encoding.decode(tokens)

def text_to_tokens(text):
    return encoding.encode(text)

def tokens_to_text(tokens):
    return encoding.decode(tokens)