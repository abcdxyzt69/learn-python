from . import helpers

# Cấu hình
prompt = "tạo 5 catchy youtube title về TFT bằng tiếng Việt"
model = "meta-llama/llama-4-maverick:free"  # FREE model

print(f"Prompt: {prompt}")
print(f"Model: {model}\n")

try:
    # Gọi ChatGPT
    response = helpers.generate_text_with_openai(prompt, model)

    print("=== KẾT QUẢ ===")
    print(response)

    # Tính cost
    model_name = model.split("/")[-1]
    cost = helpers.estimate_cost(model_name, prompt, response)

    print("\n=== CHI PHÍ ===")
    print(f"Model hiện tại: {cost['model']}")
    print(
        f"Tokens: {cost['total_tokens']} (Input: {cost['input_tokens']}, Output: {cost['output_tokens']})"
    )
    print(f"Chi phí: ${cost['total_cost_usd']} USD = {cost['total_cost_vnd']} VNĐ")

    print("\n=== NẾU DÙNG PAID MODELS (CÙng tokens) ===")
    print(f"GPT-3.5-Turbo : ${cost['if_gpt35_usd']} USD = {cost['if_gpt35_vnd']} VNĐ")
    print(
        f"GPT-4o-Mini   : ${cost['if_gpt4mini_usd']} USD = {cost['if_gpt4mini_vnd']} VNĐ"
    )
    print(f"GPT-4         : ${cost['if_gpt4_usd']} USD = {cost['if_gpt4_vnd']} VNĐ")

except Exception as e:
    print("Lỗi: " + str(e))
