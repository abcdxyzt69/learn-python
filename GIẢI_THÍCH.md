# 🕷️ GIẢI THÍCH WEB SCRAPING ĐỠN GIẢN

## 📖 Code của bạn làm gì?

```python
from bs4 import BeautifulSoup
import requests
```
**Nhập thư viện:**
- `requests`: Gửi yêu cầu đến website để lấy HTML
- `BeautifulSoup`: Phân tích HTML để tìm thông tin cần thiết

---

## 🔍 Các bước chính

### Bước 1: Lấy HTML từ website
```python
response = requests.get(url, timeout=10)
```
- Gửi request đến `https://www.python.org/jobs/`
- Giống như bạn mở website trên trình duyệt
- `timeout=10`: Chờ tối đa 10 giây

### Bước 2: Parse (phân tích) HTML
```python
soup = BeautifulSoup(response.text, "html.parser")
```
- Chuyển HTML thô thành cấu trúc dễ tìm kiếm
- Giống như "đọc hiểu" trang web

### Bước 3: Tìm các elements cần thiết
```python
job_posts = soup.find_all("h2", class_="listing-company")
```
- Tìm TẤT CẢ thẻ `<h2>` có `class="listing-company"`
- Trả về danh sách các elements tìm thấy

### Bước 4: Lấy dữ liệu
```python
link = job_post.find("a")
if link:
    company_name = link.text.strip()
    print(company_name)
```
- Tìm thẻ `<a>` (link) trong mỗi job post
- Lấy text bên trong
- `.strip()`: Xóa khoảng trắng thừa

---

## ⚠️ Các điểm quan trọng

### 1. Luôn check `None`
```python
# ❌ SAI - Sẽ crash nếu không tìm thấy
company = job_post.find("a").text

# ✅ ĐÚNG - An toàn
link = job_post.find("a")
if link:
    company = link.text
```

### 2. Xử lý lỗi
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Kiểm tra status code
except requests.exceptions.Timeout:
    print("Timeout!")
except requests.exceptions.ConnectionError:
    print("Không kết nối được!")
```

### 3. Clean dữ liệu
```python
text = link.text.strip()  # Xóa spaces, \n, \t
```

---

## 🎯 Tóm tắt nhanh

```
1. requests.get()        → Lấy HTML từ website
2. BeautifulSoup()       → Parse HTML
3. soup.find_all()       → Tìm elements
4. element.text          → Lấy text
5. .strip()              → Clean text
```

---

## 🛠️ Các method hay dùng

### Tìm kiếm
```python
soup.find("h1")                          # Tìm 1 cái đầu tiên
soup.find_all("h2")                      # Tìm tất cả
soup.find("div", class_="name")          # Tìm theo class
soup.find("div", id="header")            # Tìm theo id
soup.find("a", href="/jobs")             # Tìm theo attribute
```

### Lấy dữ liệu
```python
element.text                    # Lấy text
element.get("href")            # Lấy attribute
element["href"]                # Cách khác
element.find("a")              # Tìm con
element.find_next("p")         # Tìm element tiếp theo
```

---

## 💡 Tips

1. **Inspect HTML trước** (F12 trên browser)
2. **Test với 1 item** trước khi loop
3. **Luôn check None** trước khi access
4. **Thêm delay** nếu scrape nhiều pages: `time.sleep(1)`
5. **Đọc robots.txt**: `website.com/robots.txt`

---

## ✅ Checklist khi scrape

- [ ] Thêm `timeout` cho requests
- [ ] Dùng `try-except` để handle lỗi
- [ ] Check `None` trước khi `.text` hoặc `.get()`
- [ ] Dùng `.strip()` để clean text
- [ ] Test với vài items trước
- [ ] Thêm delay giữa requests (nếu nhiều)
- [ ] Kiểm tra robots.txt

---

## 🚀 Nâng cao (nếu cần)

### Lưu vào file
```python
with open("results.txt", "w", encoding="utf-8") as f:
    f.write(company_name + "\n")
```

### Thêm User-Agent (tránh bị block)
```python
headers = {"User-Agent": "Mozilla/5.0 ..."}
response = requests.get(url, headers=headers)
```

### Delay giữa requests
```python
import time
time.sleep(1)  # Chờ 1 giây
```

---

**Vậy thôi! Đơn giản mà! 🎉**