import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ הגדרות עמוד מורחבות
st.set_page_config(
    page_title="Enterprise License Optimization AI", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 עיצוב מודרני ונקי (יישור לימין, כרטיסים ואפקטים של ריחופים)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: #f8fafc;
    }
    
    /* עיצוב כרטיסים מקצועי */
    .custom-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* כפתור הנעה לפעולה משודרג */
    button[kind="primary"] {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.4);
    }
    
    /* שיפור מראה הטאבים */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
        color: #94a3b8;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #10b981;
    }
    .stTabs [aria-selected="true"] {
        color: #10b981 !important;
        border-bottom-color: #10b981 !important;
    }
    
    /* לינק הורדה מעוצב ככפתור משני */
    .download-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #334155;
        color: #f8fafc !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        transition: background 0.2s;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .download-btn:hover {
        background-color: #475569;
    }
</style>
""", unsafe_allow_html=True)

# ✅ כותרת המערכת
st.markdown("<h1 style='text-align: center; color: #10b981;'>🛡️ SAM Agent Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem;'>מערכת סוכנים חכמה לאופטימיזציה וניהול נכסי רישוי ארגוניים</p>", unsafe_allow_html=True)
st.markdown("---")

# ✅ אימות מפתח API מה-Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) לא נמצא ב-Secrets של האפליקציה.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ טעינת קובץ והצגת נתונים מהירה
uploaded_file = st.file_uploader("📁 גררי או בחרי את קובץ הרישוי של הארגון", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("✅ הקובץ נטען בהצלחה במערכת")
        
        # 📊 תצוגת מדדים מהירה (Metrics) המבוססת על הקובץ שהועלה
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="סה\"כ שורות נתונים", value=f"{df.shape[0]:,}")
        with col2:
            st.metric(label="עמודות שזוהו", value=df.shape[1])
        with col3:
            # ניסיון חילוץ עמודה פיננסית אם קיימת, לטובת מראה יוקרתי
            cost_cols = [c for c in df.columns if 'מחיר' in c or 'עלות' in c or 'cost' in c.lower() or 'price' in c.lower()]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.metric(label="סך תקציב נומינלי מזוהה", value=f"₪{total_cost:,.2f}")
            else:
                st.metric(label="סטטוס קובץ", value="תקין וממתין לניתוח")

        # הצגת הצצה לנתונים בתוך קונטיינר מעוצב
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 הצצה לנתוני הגלם (10 שורות ראשונות)")
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        table_as_text = df.to_string(index=False)

    except Exception as e:
        st.error(f"שגיאה בקריאת הקובץ: {e}")
        st.stop()
else:
    st.info("⬅️ אנא העלי קובץ נתונים (CSV או Excel) כדי להפעיל את סוכני ה-AI.")
    st.stop()

# ✅ הפעלת מערכת הסוכנים
st.markdown("### 🤖 הפעלת ארכיטקטורת הסוכנים")
if st.button("🚀 הפעל סוכני ניתוח ואסטרטגיה", type="primary"):
    
    # 🕵️‍♂️ סוכן 1 - אנליסט הנתונים החוקר
    # שימוש ב-system_instruction כדי לקבע את ההתנהגות המקצועית שלו
    analyst_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="אתה אנליסט בכיר לניהול נכסי תוכנה (SAM Expert). תפקידך לנתח קבצי נתונים, למצוא חריגות, כפילויות, רישיונות שלא בשימוש, וסיכוני תאימות משפטית או כלכלית. ענה בעברית מקצועית, והשתמש בטבלאות Markdown ובכותרות ברורות."
    )
    
    analyst_prompt = f"להלן נתוני הרישוי הגולמיים של הארגון. בצע ניתוח מעמיק והפק דוח ממצאים מפורט:\n\n{table_as_text}"
    
    with st.spinner("🕵️‍♂️ סוכן 1: אנליסט הנתונים סורק את הקובץ ומאתר חריגות..."):
        res1 = analyst_model.generate_content(analyst_prompt)
        analyst_report = res1.text

    # 🛠️ סוכן 2 - הארכיטקט האסטרטגי
    # הסוכן השני מקבל את הפלט של הראשון ומסיק ממנו מסקנות ניהוליות
    architect_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="אתה ארכיטקט מערכות ומנהל טכנולוגיות בכיר (CTO). תפקידך לקחת דוחות אנליטיים גולמיים ולהפוך אותם לתוכנית עבודה אסטרטגית, המלצות פיננסיות ברורות לחיסכון, וטקסט מוכן להצגה להנהלה הבכירה (Executive Summary). ענה בעברית עסקית רהוטה."
    )
    
    architect_prompt = f"בהתבסס על דוח הממצאים של האנליסט, בנה תוכנית פעולה אסטרטגית, המלצות לחיסכון מעשי, וניסוח סיכום מנהלים רשמי:\n\n{analyst_report}"
    
    with st.spinner("🛠️ סוכן 2: הארכיטקט האסטרטגי מגבש תוכנית פעולה והמלצות פיננסיות..."):
        res2 = architect_model.generate_content(architect_prompt)
        architect_report = res2.text

    # 🌟 הצגת התוצרים בצורה היררכית ומקצועית (Tabs)
    st.markdown("### 📊 תוצרי המערכת")
    tab1, tab2 = st.tabs(["📋 דוח אנליסט (ממצאים וחריגות)", "🎯 תוכנית אסטרטגית (המלצות ומנהלים)"])
    
    with tab1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown(analyst_report)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown(architect_report)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 📥 יצירת קובץ דוח מאוחד להורדה
    full_report = f"=========================================\nENTERPRISE LICENSE OPTIMIZATION REPORT\n=========================================\n\n[PART 1: ANALYST REPORT]\n\n{analyst_report}\n\n=========================================\n[PART 2: STRATEGIC ACTION PLAN]\n\n{architect_report}"
    b64 = base64.b64encode(full_report.encode('utf-8')).decode()
    
    st.markdown("---")
    st.markdown(
        f'<div style="text-align: left;"><a class="download-btn" href="data:file/txt;base64,{b64}" download="License_Optimization_Report.txt">📥 הורדת הדוח המלא (TXT)</a></div>',
        unsafe_allow_html=True
    )
