import os
from helpers import estimate_cost, get_youtube_transcript
from llm import generate, get_service
from prompts.tft_prompts import tft_title_prompt


# # Build prompt from template
topic = "choi up cap trong meta reroll"
prompt1 = tft_title_prompt.format(topic=topic)

# Prefer A4F service by default
SERVICE_NAME = "a4f"
MODEL_OVERRIDE = os.getenv("A4F_MODEL") or None  # e.g. provider-1/chatgpt-4o-latest

service_info = get_service(SERVICE_NAME)
model_name = MODEL_OVERRIDE or service_info["default_model"]

print(f"=== TEST : {SERVICE_NAME.upper()}  ===")
print(f"Using model: {model_name}\n")

response = generate(prompt1, service=SERVICE_NAME, model=MODEL_OVERRIDE)
print(response)

print("\n=== COST ESTIMATION ===")
cost = estimate_cost(model_name, prompt1, response)

print(f"Tokens: {cost['input_tokens']} input + {cost['output_tokens']} output")
print(f"Current cost: ${cost['total_cost_usd']} (FREE)")
print("\nIf using paid models:")
print(
    f"  GPT-3.5-turbo:  ${cost['if_gpt35_usd']:<8} = {cost['if_gpt35_vnd']:>10,.0f} VND"
)
print(
    f"  GPT-4o-mini:    ${cost['if_gpt4mini_usd']:<8} = {cost['if_gpt4mini_vnd']:>10,.0f} VND"
)
print(
    f"  GPT-4:          ${cost['if_gpt4_usd']:<8} = {cost['if_gpt4_vnd']:>10,.0f} VND"
)

# get youtube transcript
print(get_youtube_transcript("https://www.youtube.com/watch?v=lrf8eE-ADiw"))
