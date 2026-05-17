import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# 🎨 הגדרות עיצוב
st.set_page_config(page_title="License Optimization AI", page_icon="🔍", layout="wide")

st.markdown("""
<style>
body {direction: RTL;}
.stApp {background-color: #0e1117; color: white;}
.block-container {padding: 2rem; border-radius: 12px; background-color: #161b22;}
h1, h2, h3 {color: #00cec9;}
.stButton button {
    background-color: #00b894;
    color: white;
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 מערכת AI לאופטימיזציית רישוי ארגוני")

st.markdown("📊 העלה קובץ רישוי (Excel / CSV / TXT) לקבלת ניתוח חכם והמלצות")

# 🔐 API רק מ-Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ לא הוגדר GEMINI_API_KEY ב‑Secrets")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# 📁 העלאת קובץ
uploaded_file = st.file_uploader(
    "📁 בחר קובץ",
    type=["xlsx", "xls", "csv", "txt"]
)

# ✅ בדיקה אם אין קובץ
if not uploaded_file:
    st.warning("⬅️ העלה קובץ כדי להתחיל")
    st.stop()

# 📊 קריאת קובץ לפי סוג
try:
    ext = uploaded_file.name.split(".")[-1].lower()

    if ext in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)

    elif ext == "csv":
        df = pd.read_csv(uploaded_file)

    elif ext == "txt":
        df = pd.read_csv(uploaded_file, delimiter=None)

    else:
        st.error("❌ פורמט לא נתמך")
        st.stop()

except Exception as e:
    st.error(f"❌ שגיאה בקריאת הקובץ: {e}")
    st.stop()

# ✅ תצוגה
st.success("✅ הקובץ נטען בהצלחה")
st.dataframe(df, use_container_width=True)

# ✅ המרה לטקסט
table_text = df.to_string(index=False)

# 🚀 כפתור ניתוח
if st.button("🚀 נתח נתונים"):

    try:
        # 🧠 Agent 1
        with st.spinner("🧠 מנתח נתונים..."):
            res1 = model.generate_content(f"""
            נתח את טבלת הרישוי הבאה בצורה מקצועית:
            
            {table_text}
            
            מצא:
            - כפילויות
            - רישוי מיותר
            - חריגות שימוש
            - חוסר ניצול
            """)

            analyst_report = res1.text

        # 🛠️ Agent 2
        with st.spinner("🛠️ בונה תוכנית פעולה..."):
            res2 = model.generate_content(f"""
            בהתבסס על הדוח הבא, בנה:
            
            1. תוכנית אופטימיזציה
            2. המלצות אופרטיביות
            3. צעדים לחיסכון כספי
            4. ניסוח הודעה למנהלים
            
            דוח:
            {analyst_report}
            """)

            architect_report = res2.text

        # 📊 הצגה
        tab1, tab2 = st.tabs(["📋 ניתוח", "🚀 תוכנית פעולה"])

        with tab1:
            st.markdown(analyst_report)

        with tab2:
            st.markdown(architect_report)

        # 💾 הורדה
        full_report = f"{analyst_report}\n\n{architect_report}"
        b64 = base64.b64encode(full_report.encode()).decode()

        st.markdown(
            f'<a href="data:file/txt;base64,{b64}" download="AI_Report.txt">📥 הורד דוח</a>',
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"❌ שגיאה בהרצת AI: {e}")
