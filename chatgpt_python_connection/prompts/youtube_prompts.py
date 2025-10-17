# YouTube Content Prompts

# YouTube Title Generator
youtube_title_prompt = """Tạo 5 tiêu đề YouTube hấp dẫn về [{topic}].
Tiêu đề phải:
- Có chữ thường và CHỮ HOA
- Dưới 70 ký tự
- Tạo sự tò mò
- Có từ khóa SEO"""

# YouTube Description
youtube_description_prompt = """Viết mô tả YouTube cho video về [{topic}].
Bao gồm:
- Giới thiệu ngắn gọn (2-3 câu)
- 5 bullet points chính
- 3-5 hashtags liên quan
- Call to action"""

# YouTube Thumbnail Text
youtube_thumbnail_prompt = """Tạo 3 gợi ý text ngắn gọn (3-5 từ) để đặt lên thumbnail YouTube cho video về [{topic}].
Text phải:
- Ngắn, súc tích
- Gây tò mò
- Dễ đọc từ xa"""

# YouTube Hook (first 15 seconds)
youtube_hook_prompt = """Viết hook (15 giây đầu) cho video YouTube về [{topic}].
Hook phải:
- Ngắn gọn (2-3 câu)
- Giữ chân người xem
- Hứa hẹn giá trị rõ ràng"""

# Youtube summarization from transript
youtube_summarization_prompt = """Bạn là chuyên gia về tóm tắt video, hãy tóm tắt video này: {transript} một cách ngắn gọn và rõ ràng, bao gồm các chi tiết quan trọng và ý nghĩa của video. Hãy đảm bảo rằng tóm tắt giữ được nội dung chính của video và không bỏ qua bất kỳ thông tin quan trọng nào."""
