import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai
import plotly.express as px

# ✅ הגדרות
st.set_page_config(page_title="AI License Dashboard", layout="wide")

# 🎨 CSS מתקדם
st.markdown("""
<style>
body {direction: RTL;}
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e2e8f0;
}
.block-container {
    padding: 2rem;
}
h1 {
    text-align: center;
    color: #38bdf8;
}
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.stButton button {
    width: 100%;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border-radius: 10px;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ✅ כותרת
st.title("📊 מערכת AI לניהול רישוי ארגוני")

# 🔐 API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ חסר API ב‑Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# 📁 Upload
st.markdown("### 📁 העלאת קובץ")

uploaded_file = st.file_uploader("", type=["xlsx","xls","csv","txt"])

if not uploaded_file:
    st.info("⬅️ העלה קובץ כדי להתחיל")
    st.stop()

# ✅ קריאה
ext = uploaded_file.name.split(".")[-1]

if ext in ["xlsx", "xls"]:
    df = pd.read_excel(uploaded_file)
elif ext == "csv":
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv(uploaded_file, delimiter=None)

# ✅ תצוגה יפה
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 נתונים")
    st.dataframe(df, use_container_width=True)

with col2:
    st.markdown("### 📊 סקירה מהירה")

    try:
        num_cols = df.select_dtypes(include='number').columns

        if len(num_cols) > 0:
            chart = px.bar(df, y=num_cols[0])
            st.plotly_chart(chart, use_container_width=True)
    except:
        st.info("אין נתונים מספריים לגרף")

# ✅ טקסט ל-AI
table_text = df.to_string(index=False)

# 🚀 כפתור
if st.button("🚀 ניתוח חכם"):

    with st.spinner("🧠 מנתח נתונים..."):

        res1 = model.generate_content(f"""
        נתח את הנתונים הבאים:
        {table_text}

        מצא:
        - בזבוזים
        - כפילויות
        - חריגות
        """)

        report1 = res1.text

    with st.spinner("🛠️ מייצר המלצות..."):

        res2 = model.generate_content(f"""
        על בסיס זה בנה תוכנית פעולה:
        {report1}
        """)

        report2 = res2.text

    st.markdown("---")

    tab1, tab2 = st.tabs(["📋 ניתוח", "🚀 המלצות"])

    with tab1:
        st.markdown(f"<div class='card'>{report1}</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown(f"<div class='card'>{report2}</div>", unsafe_allow_html=True)

    # 💾 הורדה
    full = report1 + "\n\n" + report2
    b64 = base64.b64encode(full.encode()).decode()

    st.markdown(
        f'<a href="data:file/txt;base64,{b64}" download="report.txt">📥 הורד דוח</a>',
        unsafe_allow_html=True
    )
