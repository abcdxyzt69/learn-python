# Code Generation Prompts

# General Code Generator
code_generate_prompt = """Viết code {language} để {task}.
Yêu cầu:
- Code ngắn gọn, dễ hiểu
- Có comments giải thích
- Follow best practices
- Chỉ trả về code, không giải thích dài dòng"""

# Debug Helper
code_debug_prompt = """Code này bị lỗi:

{code}

Lỗi: {error}

Hãy:
- Tìm nguyên nhân
- Đưa ra solution
- Giải thích tại sao"""
