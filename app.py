import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ 1. הגדרות מערכת מתקדמות
st.set_page_config(
    page_title="SAM OS — Neural Governance", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 2. ארכיטקטורת עיצוב פרימיום (SaaS Next-Gen UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Assistant:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Assistant', 'Plus Jakarta Sans', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* רקע קוונטי עמוק */
    .stApp {
        background: radial-gradient(140% 100% at top right, #090d16 0%, #05070c 50%, #020305 100%);
        color: #f8fafc;
    }
    
    /* מכולות זכוכית מעוגלות (Glassmorphism Pro) */
    .app-card {
        background: rgba(13, 20, 35, 0.45);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .app-card:hover {
        transform: translateY(-4px) scale(1.005);
        border-color: rgba(6, 182, 212, 0.2);
        box-shadow: 0 30px 60px -20px rgba(6, 182, 212, 0.15);
    }
    
    /* מדדים מהירים בעיצוב אפליקטיבי */
    .metric-box {
        border-right: 4px solid #06b6d4;
        padding-right: 15px;
        margin: 10px 0;
    }
    
    /* כפתור הפעלה ראשי הולוגרפי */
    button[kind="primary"] {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        border: none !important;
        border-radius: 16px !important;
        color: #020617 !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        padding: 1rem 2.5rem !important;
        cursor: pointer;
        transition: all 0.4s ease !important;
        box-shadow: 0 0 30px rgba(79, 172, 254, 0.3) !important;
        width: 100%;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.6) !important;
    }
    
    /* טאבים בסגנון תפריט אפליקציה */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
        color: #64748b;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 10px 24px;
        margin-left: 8px;
        border: 1px solid transparent;
        transition: all 0.3s;
    }
    .stTabs [aria-selected="true"] {
        color: #00f2fe !important;
        background: rgba(0, 242, 254, 0.08) !important;
        border-color: rgba(0, 242, 254, 0.2) !important;
    }
    
    /* כפתור הורדה מעוצב כפתור משני יוקרתי */
    .download-action {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 14px 32px;
        background: rgba(255, 255, 255, 0.03);
        color: #f8fafc !important;
        text-decoration: none;
        border-radius: 14px;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
    }
    .download-action:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #00f2fe;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ⚡ 3. כותרת ומבנה עליון (App Header)
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; padding: 15px 0; margin-bottom: 30px;'>
    <div>
        <span style='background: rgba(0, 242, 254, 0.1); color: #00f2fe; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 800; letter-spacing: 1px;'>AGENTIC PLATFORM v2.5</span>
        <h1 style='font-weight: 800; font-size: 2.8rem; margin: 10px 0 5px 0; background: linear-gradient(90deg, #ffffff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>SAM OS</h1>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>ניהול חוקיות רישוי ומקרי קצה בארכיטקטורת סוכנים נוירולוגית</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ 4. אימות קונפיגורציית AI
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר ב-Secrets הארגוניים.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ 5. אזור העלאה קומפקטי ואפליקטיבי
uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.toast("🎯 קובץ הנתונים נטען ומופה בהצלחה", icon="⚡")
        
        # 📊 לוח מחוונים אנליטי מהיר (Quick Metrics Dashboard)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-box'><span style='color:#64748b; font-size:0.9rem;'>רשומות מזוהות</span><br><b style='font-size:1.8rem; color:#fff;'>{df.shape[0]:,}</b></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box'><span style='color:#64748b; font-size:0.9rem;'>פרמטרים מנוהלים</span><br><b style='font-size:1.8rem; color:#fff;'>{df.shape[1]}</b></div>", unsafe_allow_html=True)
        with col3:
            cost_cols = [c for c in df.columns if any(w in c.lower() for w in ['מחיר', 'עלות', 'cost', 'price'])]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.markdown(f"<div class='metric-box'><span style='color:#00f2fe; font-size:0.9rem;'>תקציב נומינלי בסיכון</span><br><b style='font-size:1.8rem; color:#00f2fe;'>₪{total_cost:,.0f}</b></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='metric-box'><span style='color:#e11d48; font-size:0.9rem;'>מורכבות ניתוח</span><br><b style='font-size:1.8rem; color:#e11d48;'>קריטית</b></div>", unsafe_allow_html=True)

        # הצגת טבלת המקור בתוך קארד זכוכית אפליקטיבי
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; margin-top:0; font-weight:600;'>📊 תצוגת זרם נתונים גולמי</p>", unsafe_allow_html=True)
        st.dataframe(df.head(6), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # אופטימיזציית טקסט מובנית לקבצים גדולים
        if df.shape[0] > 500:
            table_as_text = df.head(500).to_string(index=False)
        else:
            table_as_text = df.to_string(index=False)

    except Exception as e:
        st.error(f"שגיאה בעיבוד הקובץ: {e}")
        st.stop()
else:
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; border: 1px dashed rgba(255,255,255,0.1); border-radius: 24px; background: rgba(255,255,255,0.01); margin-top: 15px;'>
        <div style='font-size: 2.5rem; margin-bottom: 15px;'>📥</div>
        <h3 style='margin: 0 0 10px 0; font-weight: 600; color: #f8fafc;'>העלי קובץ רישוי ארגוני</h3>
        <p style='color: #64748b; max-width: 400px; margin: 0 auto; font-size: 0.95rem;'>גררי לכאן קובץ Excel או CSV כדי לאפשר לסוכני ה-AI למפות חריגות ומקרי קצה</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ✅ 6. הגדרת חוקי ה-Agent ומקרי הקצה המורכבים
SYSTEM_INSTRUCTION_ANALYST = """
אתה ראש צוות אנליסטים בכיר לניהול נכסי תוכנה (SAM Lead). תפקידך לבחון את קובץ הנתונים הגולמי ולזהות חריגות על פי חוקי הרישוי הנוקשים הבאים של הארגון:

1. מוצרים שאינם מיקרוסופט: שים לב למוצרים פרטניים כמו TreeSize, Canva, AMI וודא שהם מנוהלים כרישוי פרטני נפרד ולא נבלעים ברישוי הכללי.
2. סביבת GitPool: נתח האם השימוש הוא ככלי רוחבי או פרטני (קיימת מחלוקת ארגונית - שקף את הסטטוס והסיכונים).
3. רישוי שרתים ולקוחות בו זמנית (Concurrent): זהה שרתים ומערכות שבהם הרישוי מוגדר לפי כמות משתמשים מקסימלית בו-זמנית (ולא כלל ארגוני) ובדוק חריגות בכמות הלקוחות המחוברים בו"ז קבוע.
4. רכיבי תשתית ייעודיים: בדוק התאמה של רישיונות לבקרי הדפסה ותיבות מייל הצורכות רישוי פיזי או וירטואלי ברגע שהן מופעלות.
5. הגדרות וסוגי רישוי: לכל רישיון מזוהה, הגדר בבירור: מה מהות הרישוי? לכמה זמן? האם הוא משויך לפי משתמש (Per User) או לפי עמדה/מקור (Per Seat / Computer / מחשב מתחבר).
6. הבדל מערכות (מערכת סורקת VS הקצאה למשתמש): הפרד והדגש בין מערכות סרוקות (כמו סרוויס שסורק את מיקרוסופט ומציג כמה פנוי) לבין משתמש קצה פיזי שצריך לשייך לו רישיון באופן מנואל.
7. חוקי VIP (רשימת ה-50): השווה בין רשימת ה-VIP (50 משתמשים בכירים) לבין הרשימה הכללית. אם משתמש VIP מוגדר עם רישוי כפול (למשל גם E3 וגם E5 במיקרוסופט), קבע האם מדובר בהקצאה זמנית או קבועה, והתרע על כפילויות.
8. מערכות ללא שיוך אוטומטי: סמן מוצרים שאין להם אופציה לצירוף אוטומטי (כמו Canva) הדורשים מעקב קפדני.

הצג את הממצאים שלך בעברית מקצועית, תוך שימוש בטבלאות Markdown מסודרות לחריגות ובולטים ברורים.
"""

SYSTEM_INSTRUCTION_ARCHITECT = """
אתה ארכיטקט מערכות מידע ומנהל טכנולוגיות ראשי (CTO). תפקידך לקבל את דוח הממצאים וחריגות מקרי הקצה של האנליסט ולהפוך אותו לתוכנית עבודה קונקרטית, המלצות לחיסכון, וניסוח רשמי להנהלה.

עליך לבנות:
1. תוכנית אסטרטגית ליישוב המחלוקות (כגון מודל הרישוי של GitPool, וכפילויות ה-VIP של E3+E5).
2. המלצות מעשיות להתמודדות עם מערכות שאינן תומכות באוטומציה (כמו Canva, רישוי לבקרי הדפסה ותיבות מייל).
3. פתרונות ייעודיים לניהול רישיונות לפי עמדה (Per Seat) לעומת משתמש (Per User).
4. ניסוח הודעה רשמית, חדה ומקצועית המיועדת למנהלים בכירים (Executive Summary) המסכמת את הסיכונים, החיסכון הכלכלי הצפוי והצעדים הבאים.

ענה בעברית עסקית רהוטה ונקייה.
"""

# ✅ 7. אזור הפעלה אינטראקטיבי
st.markdown("<div style='margin: 10px 0 25px 0;'>", unsafe_allow_html=True)
if st.button("⚡ הפעל ארכיטקטורת סוכנים אוטונומיים", type="primary"):
    
    try:
        # סוכן 1: Data Investigator
        analyst_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ANALYST
        )
        
        analyst_prompt = f"להלן נתוני הרישוי הארגוניים של החברה. בצע סריקה קפדנית והפק דוח חריגות ומקרי קצה מלא:\n\n{table_as_text}"
        
        with st.spinner("🤖 סוכן 1 (Data Investigator) סורק מקרי קצה ותשתיות..."):
            res1 = analyst_model.generate_content(analyst_prompt)
            analyst_report = res1.text

        # סוכן 2: Strategic Architect
        architect_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ARCHITECT
        )
        
        architect_prompt = f"על בסיס דוח הממצאים המורכב ומקרי הקצה שמופו, גבש אסטרטגיית פעולה יישומית וסיכום מנהלים בכיר:\n\n{analyst_report}"
        
        with st.spinner("⚡ סוכן 2 (Strategic Architect) מגבש המלצות פיננסיות ומכתב מנהלים..."):
            res2 = architect_model.generate_content(architect_prompt)
            architect_report = res2.text

        # 🌟 8. תצוגת תוצרים אפליקטיבית (App Workspace)
        st.markdown("<p style='color: #64748b; font-weight:600; margin-bottom:15px;'>💻 סביבת עבודה אסטרטגית</p>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🎯 ממצאי אנליסט הנתונים", "💎 תוכנית אסטרטגית וניסוח למנהלים"])
        
        with tab1:
            st.markdown("<div class='app-card'>", unsafe_allow_html=True)
            st.markdown(analyst_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab2:
            st.markdown("<div class='app-card'>", unsafe_allow_html=True)
            st.markdown(architect_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 📥 יצירת קובץ דוח מעוצב להורדה
        full_report = f"=========================================\nSAM NEURAL INTELLIGENCE REPORT - EDGE CASES INCLUDED\n=========================================\n\n[PART 1: DEEP EDGE-CASE ANALYTICS]\n\n{analyst_report}\n\n=========================================\n[PART 2: STRATEGIC ACTION PLAN & EXEC SUMMARY]\n\n{architect_report}"
        b64 = base64.b64encode(full_report.encode('utf-8')).decode()
        
        st.markdown("---")
        st.markdown(
            f'<div style="text-align: left;"><a class="download-action" href="data:file/txt;base64,{b64}" download="SAM_Intelligence_Report.txt">📥 ייצוא קובץ נתונים משולב</a></div>',
            unsafe_allow_html=True
        )
        
    except Exception as api_error:
        st.error(f"❌ שגיאת רשת במערכת ה-AI: {api_error}")

st.markdown("</div>", unsafe_allow_html=True)
