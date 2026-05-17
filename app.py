import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ הגדרות עמוד מתקדמות
st.set_page_config(
    page_title="SAM AI - Advanced Optimization", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 עיצוב עתידני, קליל ומפוצץ (Next-Gen Cyberpunk UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;800&display=swap');
    
    /* הגדרות בסיס ויישור לימין */
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* רקע מדורג עמוק ומודרני */
    .stApp {
        background: radial-gradient(circle at top right, #0f172a, #020617);
        color: #f1f5f9;
    }
    
    /* כרטיסי זכוכית עתידניים (Glassmorphism) */
    .cyber-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    /* אפקט ריחוף מטורף לכרטיסים */
    .cyber-card:hover {
        transform: translateY(-5px);
        border-color: rgba(16, 185, 129, 0.3);
        box-shadow: 0 12px 40px 0 rgba(16, 185, 129, 0.1);
    }
    
    /* כפתור הפעלה סופר-פרימיום עם אנימציית זוהר */
    button[kind="primary"] {
        background: linear-gradient(90deg, #10b981, #06b6d4) !important;
        border: none !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        padding: 0.85rem 2.5rem !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2) !important;
        width: 100%;
    }
    
    button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.6) !important;
    }
    
    /* עיצוב הטאבים המרכזיים */
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        font-weight: 700;
        color: #64748b;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #06b6d4;
    }
    .stTabs [aria-selected="true"] {
        color: #10b981 !important;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 10px 10px 0 0;
    }
    
    /* כפתור הורדה מעוצב כאלמנט פרימיום צידי */
    .download-cyber {
        display: inline-block;
        padding: 12px 28px;
        background: transparent;
        color: #06b6d4 !important;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 700;
        border: 2px solid #06b6d4;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.1);
    }
    .download-cyber:hover {
        background: #06b6d4;
        color: #020617 !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ⚡ כותרת ראשית חללית
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='font-weight: 800; font-size: 3rem; background: linear-gradient(90deg, #10b981, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        ⚡ SAM NEURAL INTELLIGENCE
    </h1>
    <p style='color: #94a3b8; font-size: 1.25rem; font-weight: 300; margin-top: -10px;'>
        הדור הבא של ניתוח ואופטימיזציית רישוי ארגוני מבוסס סוכנים אוטונומיים
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ✅ בדיקת מפתח API מ-Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר ב-Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ ממשק העלאת קבצים קליל ונקי
uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("🎯 הקובץ נקלט בהצלחה במערכת. המידע מוכן לעיבוד.")
        
        # 📊 כרטיסי מדדים (Metrics) מעוצבים וקלילים
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="📊 שורות נתונים", value=f"{df.shape[0]:,}")
        with col2:
            st.metric(label="⚙️ פרמטרים שנמצאו", value=df.shape[1])
        with col3:
            cost_cols = [c for c in df.columns if any(w in c.lower() for w in ['מחיר', 'עלות', 'cost', 'price'])]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.metric(label="💰 היקף פיננסי מזוהה", value=f"₪{total_cost:,.0f}")
            else:
                st.metric(label="🛡️ רמת מורכבות קובץ", value="גבוהה (מומלץ לניתוח)")

        # תצוגת נתונים בתוך קארד זכוכית
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #06b6d4; margin-top:0;'>🔍 סקירה מהירה של נתוני המקור</h4>", unsafe_allow_html=True)
        st.dataframe(df.head(8), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        table_as_text = df.to_string(index=False)

    except Exception as e:
        st.error(f"שגיאה בטעינת הקובץ: {e}")
        st.stop()
else:
    st.markdown("""
    <div style='text-align: center; padding: 40px; border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px; background: rgba(255,255,255,0.02);'>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>גררי לכאן קובץ אקסל או CSV כדי להזניק את סוכני ה-AI</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ✅ אזור הפעלת הסוכנים
st.markdown("<div style='margin: 30px 0;'>", unsafe_allow_html=True)
if st.button("⚡ הזרק ניתוח ואופטימיזציה בזמן אמת", type="primary"):
    
    # 🕵️‍♂️ סוכן 1: Data Investigator
    analyst_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="אתה אנליסט סייבר ו-SAM בכיר. תפקידך לחשוף חוסר יעילות, כפילויות רישוי, סיכוני תאימות ובזבוז תקציבי. הצג את הממצאים שלך בצורה חדה, נקייה, מבוססת טבלאות Markdown ונקודות מפתח ברורות בעברית מקצועית."
    )
    
    analyst_prompt = f"בצע ניתוח נוירולוגי מעמיק על נתוני הרישוי הבאים ומצא חריגות:\n\n{table_as_text}"
    
    with st.spinner("🧠 סוכן 1 (Data Analyst) מפצח את מבנה הנתונים..."):
        res1 = analyst_model.generate_content(analyst_prompt)
        analyst_report = res1.text

    # 🛠️ סוכן 2: Strategic Architect
    architect_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="אתה ארכיטקט מערכות פיננסיות ו-CTO. תפקידך לקחת ממצאים גולמיים של אנליסט ולהפוך אותם לתוכנית פעולה אסטרטגית מטורפת, דרכים מהירות לחיסכון במשאבים (Quick Wins), וניסוח סיכום בכירים יוקרתי להנהלה. ענה בעברית עסקית רהוטה ונקייה."
    )
    
    architect_prompt = f"על בסיס הדוח הבא, גבש אסטרטגיית פעולה יישומית וסיכום מנהלים:\n\n{analyst_report}"
    
    with st.spinner("🚀 סוכן 2 (Strategic Architect) מייצר תוכנית אופטימיזציה פיננסית..."):
        res2 = architect_model.generate_content(architect_prompt)
        architect_report = res2.text

    # 🌟 הצגת התוצרים בטאבים עתידניים
    st.markdown("### 📊 תוצרי עיבוד הסוכנים")
    tab1, tab2 = st.tabs(["🎯 ממצאי אנליסט הנתונים", "💎 תוכנית אסטרטגית ומנהלים"])
    
    with tab1:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown(analyst_report)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        st.markdown(architect_report)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 📥 יצירת קובץ דוח מעוצב להורדה
    full_report = f"=========================================\nSAM NEURAL INTELLIGENCE REPORT\n=========================================\n\n[PART 1: DEEP ANALYTICS]\n\n{analyst_report}\n\n=========================================\n[PART 2: STRATEGIC ACTION PLAN]\n\n{architect_report}"
    b64 = base64.b64encode(full_report.encode('utf-8')).decode()
    
    st.markdown("---")
    st.markdown(
        f'<div style="text-align: left;"><a class="download-cyber" href="data:file/txt;base64,{b64}" download="SAM_Intelligence_Report.txt">📥 ייצוא דוח מלא ומסוכם</a></div>',
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)
