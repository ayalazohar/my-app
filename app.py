import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ הגדרות עמוד
st.set_page_config(page_title="License Optimization AI", page_icon="🔍", layout="wide")

st.title("🔍 מערכת סוכני AI לאופטימיזציה וניהול רישוי ארגוני")

# 🔐 ✅ חובה: API רק מ-Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ לא הוגדר GEMINI_API_KEY ב‑Secrets")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

# ✅ חיבור ל‑Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 📁 העלאת קובץ
uploaded_file = st.file_uploader("בחר קובץ אקסל", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ הקובץ נטען")
    st.dataframe(df.head())

else:
    st.info("💡 משתמש בנתוני דמו")
    df = pd.DataFrame({
        "מוצר": ["M365", "Canva", "TreeSize"],
        "כמות": [100, 20, 5],
        "בשימוש": [90, 10, 8]
    })
    st.dataframe(df)

# ✅ המרת הדאטה לטקסט
table_text = df.to_markdown(index=False)

# 🚀 כפתור הפעלה
if st.button("🚀 הרץ ניתוח AI"):

    # 🔍 Agent 1
    with st.spinner("🧠 אנליסט עובד..."):
        response1 = model.generate_content(f"""
        נתח את הנתונים הבאים:
        {table_text}
        מצא כפילויות, בזבוזים וחריגות
        """)
        analyst_report = response1.text

    # 🛠️ Agent 2
    with st.spinner("🛠️ ארכיטקט עובד..."):
        response2 = model.generate_content(f"""
        על בסיס זה בנה תוכנית פעולה:
        {analyst_report}
        """)
        architect_report = response2.text

    # 📊 תצוגה
    tab1, tab2 = st.tabs(["📋 דוח אנליסט", "🚀 תוכנית פעולה"])

    with tab1:
        st.markdown(analyst_report)

    with tab2:
        st.markdown(architect_report)

    # 💾 הורדה
    full_report = f"{analyst_report}\n\n{architect_report}"
    b64 = base64.b64encode(full_report.encode()).decode()

    st.markdown(
        f'<a href="data:file/txt;base64,{b64}" download="report.txt">📥 הורד דוח</a>',
        unsafe_allow_html=True
    )
