import requests
import newspaper as nk
import streamlit as st


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS = [
    "openrouter/auto",
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct",
]


# Ham goi OpenRouter va tra ve noi dung
def generate_text(prompt: str, model: str, api_key: str) -> str:
    prompt = prompt.strip()
    if not api_key:
        raise ValueError("Chua nhap OpenRouter API key.")
    if not prompt:
        raise ValueError("Prompt dang rong.")

    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    message = response.json()["choices"][0]["message"]["content"]
    return message.strip()


# Ham lay noi dung bai viet tu URL bang thu vien newspaper
def get_article_from_url(url: str) -> str:
    if not url.strip():
        raise ValueError("URL dang rong, hay nhap duong dan hop le.")

    article = nk.Article(url.strip())
    article.download()
    if article.download_state != 2:
        raise RuntimeError("Khong tai duoc noi dung tu URL.")

    article.parse()

    if not article.text.strip():
        raise RuntimeError("Bai viet khong co noi dung van ban.")

    return article.text.strip()


# Cong cu 1: cho phep nhap prompt va goi truc tiep OpenAI
def tool_1_prompt(api_key: str) -> None:
    st.title("Prompt Tester")
    prompt = st.text_area("Nhap Prompt:", height=200)
    model = st.selectbox("Chon model", OPENROUTER_MODELS)

    if st.button("Test") and prompt:
        try:
            with st.spinner("Dang goi OpenRouter..."):
                result = generate_text(prompt, model, api_key)
            st.success("Da nhan phan hoi tu OpenRouter!")
            st.write(result)
        except Exception as exc:
            st.error(f"Loi: {exc}")


# Cong cu 2: lay noi dung blog va tao prompt tu dong
def tool_2_blog_url(api_key: str) -> None:
    st.title("Blog AI Automator")
    blog_url = st.text_input("Nhap URL bai blog:")
    user_prompt = st.text_area(
        "Nhap huong dan cho AI (vi du: 'Tao bullet point tom tat ngan gon:')",
        height=150,
    )
    model = st.selectbox("Chon model", OPENROUTER_MODELS)

    if st.button("Generate"):
        if not blog_url.strip():
            st.warning("Hay nhap URL truoc khi nhan Generate.")
            return

        try:
            with st.spinner("Dang tai noi dung bai viet..."):
                article_text = get_article_from_url(blog_url)

            prompt = user_prompt.strip()
            prompt = f"{prompt}\n\n{article_text}" if prompt else article_text

            with st.spinner("Dang tom tat bang OpenRouter..."):
                result = generate_text(prompt, model, api_key)

            st.success("Da tao tom tat thanh cong!")
            st.markdown("### Ket qua:")
            st.write(result)
        except Exception as exc:
            st.error(f"Loi: {exc}")


def main() -> None:
    # Sidebar chua thong tin cau hinh chung
    st.sidebar.header("Settings")

    api_key = st.sidebar.text_input(
        "OpenRouter API key (bat buoc de goi AI)", type="password"
    )

    tool_selection = st.sidebar.selectbox(
        "Chon cong cu", ["Prompt Tester", "Blog AI Automator"]
    )

    if tool_selection == "Prompt Tester":
        tool_1_prompt(api_key)
    else:
        tool_2_blog_url(api_key)


if __name__ == "__main__":
    main()
