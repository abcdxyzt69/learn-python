"""
Web Scraping đơn giản - Lấy danh sách công việc Python
"""

from bs4 import BeautifulSoup
import requests

# URL trang web cần scrape
url = "https://www.python.org/jobs/"

try:
    # Bước 1: Gửi request để lấy HTML từ trang web
    # timeout=10 nghĩa là chờ tối đa 10 giây
    response = requests.get(url, timeout=10)

    # Kiểm tra xem request có thành công không (status code 200 = OK)
    response.raise_for_status()

    # Bước 2: Parse (phân tích) HTML bằng BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Bước 3: Tìm tất cả thẻ h2 có class="listing-company"
    job_posts = soup.find_all("h2", class_="listing-company")

    print(f"✅ Tìm thấy {len(job_posts)} công việc:\n")

    # Bước 4: Loop qua từng job post và in ra tên công ty
    for i, job_post in enumerate(job_posts, 1):
        # Tìm thẻ <a> trong job_post
        link = job_post.find("a")

        # Kiểm tra xem có tồn tại không (tránh lỗi)
        if link:
            company_name = link.text.strip()  # .strip() xóa khoảng trắng thừa
            print(f"{i}. {company_name}")
        else:
            print(f"{i}. [Không có tên công ty]")

except requests.exceptions.Timeout:
    print("❌ Lỗi: Mất quá nhiều thời gian để kết nối")

except requests.exceptions.ConnectionError:
    print("❌ Lỗi: Không thể kết nối đến website")

except requests.exceptions.HTTPError as e:
    print(f"❌ Lỗi HTTP: {e}")

except Exception as e:
    print(f"❌ Lỗi không xác định: {e}")

print("\n✨ Hoàn thành!")
