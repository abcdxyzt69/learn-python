import llm
from prompts import productivity_prompts

selected_service = "openrouter"
selected_model = "openai/gpt-4o-mini"
user_input = "get me the latest price of bitcoin"

prompt = productivity_prompts.auto_gpt_prototype.format(user_input=user_input)
response = llm.generate(prompt, service=selected_service, model=selected_model)
action_code = response.strip()
action_lookup = {
    "1": "Search the web for the latest price.",
    "2": "Summarize the provided information.",
    "3": "Translate the input into English.",
}

print(f"Raw model reply: {action_code}")
print(
    f"Interpreted action: {action_lookup.get(action_code, 'No valid action detected.')}"
)
