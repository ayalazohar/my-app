import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# הגדרות עמוד
st.set_page_config(page_title="License Optimization AI", page_icon="🔍", layout="wide")

st.title("🔍 מערכת סוכני AI לאופטימיזציה וניהול רישוי ארגוני")

# 🔐 טעינת API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("הזיני Gemini API Key:", type="password")

if not api_key:
    st.warning("יש להזין API KEY כדי להמשיך")
    st.stop()

# ✅ חיבור ל‑Gemini (תיקון חשוב!)
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 📁 העלאת קובץ
uploaded_file = st.file_uploader("בחרי קובץ אקסל", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("הקובץ נטען ✅")
    st.dataframe(df.head())

else:
    df = pd.DataFrame({
        "מוצר": ["M365", "Canva", "TreeSize"],
        "כמות": [100, 20, 5],
        "בשימוש": [90, 10, 8]
    })
    st.info("מציג דאטה לדוגמה")
    st.dataframe(df)

# המרת טבלה לטקסט
table_text = df.to_markdown(index=False)

# 🚀 כפתור הפעלה
if st.button("הרץ AI"):
    
    with st.spinner("אנליסט עובד..."):
        response1 = model.generate_content(f"""
        נתח את הנתונים:
        {table_text}
        מצא בעיות רישוי וכפילויות
        """)
        analyst_report = response1.text

    with st.spinner("ארכיטקט עובד..."):
        response2 = model.generate_content(f"""
        על בסיס זה בנה תוכנית פעולה:
        {analyst_report}
        """)
        architect_report = response2.text

    # 🧾 טאבים
    tab1, tab2 = st.tabs(["דוח אנליסט", "תוכנית עבודה"])

    with tab1:
        st.markdown(analyst_report)

    with tab2:
        st.markdown(architect_report)

    # 💾 הורדה
    full_report = f"{analyst_report}\n\n{architect_report}"
    b64 = base64.b64encode(full_report.encode()).decode()

    href = f'<a href="data:file/txt;base64,{b64}" download="report.txt">📥 הורד דוח</a>'
    st.markdown(href, unsafe_allow_html=True)
