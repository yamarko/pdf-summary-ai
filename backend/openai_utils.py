import os
import logging
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError
import tiktoken
from fastapi import HTTPException

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=0)

CHUNK_MAX_TOKENS = int(os.getenv("CHUNK_MAX_TOKENS", 5000))
SUMMARY_MAX_TOKENS = int(os.getenv("SUMMARY_MAX_TOKENS", 200))


def chunk_text(text: str, model: str, max_tokens: int = CHUNK_MAX_TOKENS) -> list[str]:
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)

    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i : i + max_tokens]
        chunks.append(encoding.decode(chunk_tokens))
    return chunks


def call_openai_summary(prompt: str, model: str, max_tokens: int) -> str:
    retries = 8
    delay = 5

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_completion_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()

        except RateLimitError as e:
            if attempt < retries - 1:
                logger.warning(
                    f"Rate limit hit. Retrying in {delay} seconds... (attempt {attempt+1}/{retries})"
                )
                time.sleep(delay)
            else:
                raise HTTPException(
                    status_code=429,
                    detail="OpenAI API rate limit exceeded after retries.",
                )
        except APIError as e:
            raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def generate_summary(text: str, max_tokens: int = SUMMARY_MAX_TOKENS) -> str:
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text to summarize.")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    chunks = chunk_text(text, model=model, max_tokens=CHUNK_MAX_TOKENS)

    partial_summaries = []
    for idx, chunk in enumerate(chunks, start=1):
        logger.info(f"Summarizing chunk {idx}/{len(chunks)}...")
        prompt = f"Summarize the following text concisely in a paragraph:\n{chunk}"
        summary_chunk = call_openai_summary(prompt, model=model, max_tokens=max_tokens)
        partial_summaries.append(summary_chunk)

    if len(partial_summaries) > 1:
        combined_text = "\n\n".join(partial_summaries)
        logger.info("Generating final summary from partial results...")
        prompt = f"Summarize the following summaries into a concise final summary:\n{combined_text}"
        final_summary = call_openai_summary(prompt, model=model, max_tokens=max_tokens)
        return final_summary

    return partial_summaries[0]
