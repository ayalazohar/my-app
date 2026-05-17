import streamlit as st
import pandas as pd
import google.generativeai as genai

# ✅ CONFIG
st.set_page_config(page_title="License AI Copilot", layout="wide")

# 🎨 UI מודרני (כמו ChatGPT)
st.markdown("""
<style>
body {direction: RTL;}

.stApp {
    background: #0f172a;
    color: #e2e8f0;
}

/* Chat container */
.chat-box {
    max-width: 800px;
    margin: auto;
}

/* Messages */
.user-msg {
    background: #2563eb;
    padding: 12px 16px;
    border-radius: 14px;
    margin: 10px 0;
    color: white;
    align-self: flex-end;
}

.ai-msg {
    background: #1e293b;
    padding: 12px 16px;
    border-radius: 14px;
    margin: 10px 0;
}

/* Header */
.header {
    text-align:center;
    margin-bottom:20px;
}
.header-title {
    font-size:32px;
    font-weight:700;
}
.header-sub {
    color:#94a3b8;
}
</style>
""", unsafe_allow_html=True)

# 🔐 API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing API key")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ HEADER
st.markdown("""
<div class="header">
    <div class="header-title">🤖 License AI Copilot</div>
    <div class="header-sub">ניתוח רישוי ארגוני באמצעות AI</div>
</div>
""", unsafe_allow_html=True)

# ✅ Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

# ✅ Upload
uploaded_file = st.file_uploader("📁 העלה קובץ רישוי", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith("xlsx"):
        st.session_state.df = pd.read_excel(uploaded_file)
    else:
        st.session_state.df = pd.read_csv(uploaded_file)

    st.success("✅ קובץ נטען")

# ✅ Chat UI
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-msg'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ✅ Input
user_input = st.text_input("שאל משהו על הרישוי...")

if user_input:

    # שמירת הודעת משתמש
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # ✅ AI answer
    if st.session_state.df is not None:

        data_text = st.session_state.df.to_string(index=False)

        prompt = f"""
        אתה מומחה לניהול רישוי ארגוני.
        יש לך את הנתונים הבאים:

        {data_text}

        שאלה:
        {user_input}

        תן תשובה חכמה מקצועית.
        """

    else:
        prompt = user_input

    with st.spinner("חושב..."):
        response = model.generate_content(prompt)
        answer = response.text

    # שמירת תשובת AI
    st.session_state.messages.append({
        "role": "ai",
        "content": answer
    })

    st.rerun()
