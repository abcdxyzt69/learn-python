from helpers import get_article_from_url
from llm import llm_generate_text
from prompts.blog_prompts import blog_bullet_summary_prompt


def summarize_blog(
    url="https://learnwithhasan.com/chatgpt-earthquake/",
    min_points=5,
    max_points=10,
    service="OpenAI",
    model="gpt-3.5-turbo",
):
    article = get_article_from_url(url)
    prompt = blog_bullet_summary_prompt.format(
        MinPoints=min_points, MaxPoints=max_points, InputText=article
    )
    return llm_generate_text(prompt, service, model)


if __name__ == "__main__":
    print(summarize_blog())
