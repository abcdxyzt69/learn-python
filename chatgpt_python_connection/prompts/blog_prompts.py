blog_bullet_summary_prompt = """You are a helpful assistant that summarizes blog posts.

Please read the article text and produce concise bullet points that capture the key ideas in Vietnamese.
- Write between {MinPoints} and {MaxPoints} bullets.
- Use clear, short sentences so a busy reader can scan the summary quickly.
- Preserve any critical facts, figures, or quotes if they appear.

Blog Article:
{InputText}
"""
