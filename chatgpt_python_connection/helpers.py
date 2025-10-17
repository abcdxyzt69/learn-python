import re
from typing import List, Optional

import requests
import tiktoken
from bs4 import BeautifulSoup
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

api_key = "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"
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


def generate_text_with_openai(user_prompt, model="meta-llama/llama-4-maverick:free"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia viết YouTube title viral"},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content or ""


def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def _extract_youtube_video_id(url: str) -> Optional[str]:
    patterns = [
        r"(?:v=|/)([0-9A-Za-z_-]{11}).*",
        r"(?:embed/)([0-9A-Za-z_-]{11})",
        r"^([0-9A-Za-z_-]{11})$",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_youtube_transcript(video_url: str) -> str:
    """
    Fetch transcript text for a YouTube video.

    Args:
        video_url: full YouTube URL or plain video id.

    Returns:
        Transcript text joined into a single string.

    Raises:
        ValueError: if the video ID cannot be extracted.
        RuntimeError: if the transcript cannot be retrieved.
    """

    video_id = _extract_youtube_video_id(video_url)
    if not video_id:
        raise ValueError("Không thể lấy video ID từ URL YouTube.")

    try:
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id, languages=["vi", "en"])
    except Exception as exc:
        raise RuntimeError(f"Không thể lấy transcript: {exc}") from exc

    # Join only the non-empty segments to avoid stray spaces.
    segments = []
    for item in transcript_data:
        text = getattr(item, "text", None)
        if text:
            cleaned = text.strip()
            if cleaned:
                segments.append(cleaned)

    return " ".join(segment for segment in segments if segment)


def get_article_from_url(url: str, *, timeout: int = 10) -> str:
    """
    Fetch and return readable text content from a blog article URL.

    Args:
        url: The article URL to download.
        timeout: How long to wait for the response before failing.

    Returns:
        The article text separated by newlines.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/127.0.0.1 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find("article")

    stripped = (
        article.stripped_strings
        if article is not None
        else (
            soup.body.stripped_strings
            if soup.body is not None
            else soup.stripped_strings
        )
    )

    return "\n".join(segment for segment in stripped if segment)


def estimate_cost(model_name, input_text, output_text):
    input_tokens = count_tokens(input_text)
    output_tokens = count_tokens(output_text)

    # Giá models: free + paid
    if "free" in model_name or "llama-4-maverick" in model_name:
        input_price, output_price = 0.0, 0.0
    elif "llama-3.2" in model_name:
        input_price, output_price = 0.0, 0.0
    elif model_name == "gpt-3.5-turbo":
        input_price, output_price = 0.0005, 0.0015
    elif model_name == "gpt-4o-mini":
        input_price, output_price = 0.00015, 0.0006
    elif model_name == "gpt-4":
        input_price, output_price = 0.03, 0.06
    else:
        input_price, output_price = 0.0, 0.0

    input_cost = (input_tokens / 1000) * input_price
    output_cost = (output_tokens / 1000) * output_price
    total_cost_usd = input_cost + output_cost
    total_cost_vnd = total_cost_usd * 25000

    # Tính giá nếu dùng paid models
    cost_gpt35 = ((input_tokens / 1000) * 0.0005) + ((output_tokens / 1000) * 0.0015)
    cost_gpt4mini = ((input_tokens / 1000) * 0.00015) + (
        (output_tokens / 1000) * 0.0006
    )
    cost_gpt4 = ((input_tokens / 1000) * 0.03) + ((output_tokens / 1000) * 0.06)

    return {
        "model": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "total_cost_usd": round(total_cost_usd, 6),
        "total_cost_vnd": round(total_cost_vnd, 2),
        "if_gpt35_usd": round(cost_gpt35, 6),
        "if_gpt35_vnd": round(cost_gpt35 * 25000, 2),
        "if_gpt4mini_usd": round(cost_gpt4mini, 6),
        "if_gpt4mini_vnd": round(cost_gpt4mini * 25000, 2),
        "if_gpt4_usd": round(cost_gpt4, 6),
        "if_gpt4_vnd": round(cost_gpt4 * 25000, 2),
    }
