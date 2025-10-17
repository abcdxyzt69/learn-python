import llm
from prompts import productivity_prompts

selected_service = "openrouter"
selected_model = "openai/gpt-4o-mini"
user_prompt = "tao 3 tieu de youtube ve chu de TFT mùa 15 siêu tệ"
prompt = productivity_prompts.prompt_generator.format(user_prompt=user_prompt)
response = llm.generate(prompt, service=selected_service, model=selected_model)
print(response)
