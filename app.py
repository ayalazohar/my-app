import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

# ✅ settings
st.set_page_config(page_title="License AI", layout="wide")

# 🎨 UI מודרני
st.markdown("""
<style>
body {direction: RTL;}
.stApp {
    background-color: #0b1220;
    color: #e5e7eb;
}
.block-container {
    padding: 2rem;
}
h1 {
    color: #22c55e;
    font-weight: 700;
}
.card {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ✅ Sidebar
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("מערכת ניהול רישוי מבוססת AI")

uploaded_file = st.sidebar.file_uploader(
    "📁 העלאת קובץ",
    type=["xlsx", "csv"]
)

# 🔐 API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ אין API")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# ✅ ראשי
st.title("📊 License Intelligence Dashboard")

# ❌ אין קובץ
if not uploaded_file:
    st.info("⬅️ העלה קובץ כדי להתחיל")
    st.stop()

# ✅ קריאת קובץ
if uploaded_file.name.endswith("xlsx"):
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_csv(uploaded_file)

# ✅ KPI
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='card'>📦 רשומות<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

num_cols = df.select_dtypes(include="number").columns

if len(num_cols) > 0:
    total = df[num_cols[0]].sum()
    avg = df[num_cols[0]].mean()

    col2.markdown(f"<div class='card'>💰 סה\"כ<br><h2>{int(total)}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'>📈 ממוצע<br><h2>{round(avg,2)}</h2></div>", unsafe_allow_html=True)

# ✅ גרף
if len(num_cols) > 0:
    st.markdown("### 📊 ניתוח גרפי")
    fig = px.bar(df, y=num_cols[0], title="התפלגות נתונים")
    st.plotly_chart(fig, use_container_width=True)

# ✅ טבלה
st.markdown("### 📋 נתונים")
st.dataframe(df, use_container_width=True)

# ✅ AI
if st.button("🚀 ניתוח AI חכם"):

    table_text = df.to_string(index=False)

    with st.spinner("🧠 מנתח..."):

        res1 = model.generate_content(
            f"נתח את הנתונים הארגוניים הבאים ומצא בעיות רישוי:\n{table_text}"
        )
        analysis = res1.text

    with st.spinner("🛠️ בונה אסטרטגיה..."):

        res2 = model.generate_content(
            f"בהתבסס על זה בנה תוכנית פעולה:\n{analysis}"
        )
        strategy = res2.text

    tab1, tab2 = st.tabs(["📋 ניתוח", "🚀 המלצות"])

    with tab1:
        st.markdown(analysis)

    with tab2:
        st.markdown(strategy)
