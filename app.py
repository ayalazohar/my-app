import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ 1. הגדרות מערכת וארכיטקטורת עמוד
st.set_page_config(
    page_title="SAM Core — Autonomous Optimization", 
    page_icon="🔮", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 2. ממשק עיצוב עילית (SaaS Ultra-Modern Tech UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&family=Assistant:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* רקע קוונטי מינימליסטי חלק */
    .stApp {
        background: #030712;
        color: #f3f4f6;
    }
    
    /* קונטיינרים דקיקים עם חיתוך לייזר (Tech Cards) */
    .tech-card {
        background: #0b0f19;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .tech-card:hover {
        border-color: #06b6d4;
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.15);
    }
    
    /* תיבות מדדים קומפקטיות בסגנון Dashboard מתקדם */
    .data-indicator {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px;
        text-align: right;
    }
    
    /* כפתור הפעלה טכנולוגי מרהיב עם אפקט זוהר משתנה */
    button[kind="primary"] {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #030712 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 0.8rem 2rem !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.2) !important;
        width: 100%;
    }
    
    button[kind="primary"]:hover {
        transform: scale(1.01);
        box-shadow: 0 0 35px rgba(6, 182, 212, 0.5) !important;
    }
    
    /* טאבים שטוחים בסגנון תפריטי פיתוח מודרניים */
    .stTabs [data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
        color: #9ca3af;
        background: transparent;
        border: none;
        padding: 12px 20px;
        transition: color 0.2s;
    }
    .stTabs [aria-selected="true"] {
        color: #06b6d4 !important;
        border-bottom: 2px solid #06b6d4 !important;
    }
    
    /* עיצוב רכיבי הנתונים והטבלאות של האקסל */
    [data-testid="stDataFrame"] {
        background: #0b0f19 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    
    /* כפתור הורדה ייחודי חלק ורך */
    .action-link {
        display: inline-flex;
        align-items: center;
        padding: 10px 24px;
        background: #111827;
        color: #f3f4f6 !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #374151;
        transition: all 0.2s ease;
    }
    .action-link:hover {
        background: #1f2937;
        border-color: #06b6d4;
    }
</style>
""", unsafe_allow_html=True)

# ⚡ 3. כותרת נקייה וממוקדת (Workspace Header)
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f2937; padding-bottom: 20px; margin-bottom: 30px;'>
    <div>
        <h1 style='font-weight: 800; font-size: 2.2rem; margin: 0; color: #ffffff;'>SAM CORE <span style='color: #06b6d4; font-weight: 400; font-size: 1.5rem;'>// Enterprise</span></h1>
        <p style='color: #9ca3af; font-size: 1rem; margin: 5px 0 0 0;'>ניהול חוקיות רישוי ומקרי קצה בארכיטקטורת סוכנים סינפטית</p>
    </div>
    <div style='text-align: left;'>
        <span style='border: 1px solid #06b6d4; color: #06b6d4; padding: 6px 14px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; font-family: \"JetBrains Mono\", monospace;'>SYSTEM: ONLINE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ 4. אימות קונפיגורציית AI מול Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר במערכת.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ 5. סביבת טעינת קבצים קומפקטית
uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.toast("🎯 דאטה-סט נטען בהצלחה לזיכרון המערכת", icon="⚡")
        
        # 📊 פאנל אינדיקטורים מהיר (Analytical Indicators)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='data-indicator'><span style='color:#9ca3af; font-size:0.85rem;'>שורות במטריצה</span><br><b style='font-size:1.6rem; color:#fff; font-family:\"JetBrains Mono\";'>{df.shape[0]:,}</b></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='data-indicator'><span style='color:#9ca3af; font-size:0.85rem;'>מאפיינים מזוהים</span><br><b style='font-size:1.6rem; color:#fff; font-family:\"JetBrains Mono\";'>{df.shape[1]}</b></div>", unsafe_allow_html=True)
        with col3:
            cost_cols = [c for c in df.columns if any(w in c.lower() for w in ['מחיר', 'עלות', 'cost', 'price'])]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.markdown(f"<div class='data-indicator'><span style='color:#06b6d4; font-size:0.85rem;'>חשיפה תקציבית</span><br><b style='font-size:1.6rem; color:#06b6d4; font-family:\"JetBrains Mono\";'>₪{total_cost:,.0f}</b></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='data-indicator'><span style='color:#f43f5e; font-size:0.85rem;'>רמת סיכון</span><br><b style='font-size:1.6rem; color:#f43f5e;'>חריגה</b></div>", unsafe_allow_html=True)

        # הצגת גיליון הנתונים במראה אקסל נקי ומקצועי
        st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
        st.dataframe(df.head(6), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # אופטימיזציית גודל נתונים
        if df.shape[0] > 500:
            table_as_text = df.head(500).to_string(index=False)
        else:
            table_as_text = df.to_string(index=False)

    except Exception as e:
        st.error(f"שגיאה בקריאת המקור: {e}")
        st.stop()
else:
    st.markdown("""
    <div style='text-align: center; padding: 50px 20px; border: 1px dashed #374151; border-radius: 16px; background: #0b0f19; margin-top: 15px;'>
        <span style='font-size: 2rem; color: #4b5563;'>📂</span>
        <h3 style='margin: 10px 0 5px 0; font-weight: 600; color: #ffffff; font-size: 1.1rem;'>הזנת מקור נתונים</h3>
        <p style='color: #9ca3af; font-size: 0.9rem; margin: 0;'>משוך קובץ Excel או CSV לכאן להפעלת מערך הסוכנים</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# 🧠 6. קביעת הגדרות חוקיות ומקרי קצה עבור הסוכנים האוטונומיים
SYSTEM_INSTRUCTION_ANALYST = """
אתה ראש צוות אנליסטים בכיר לניהול נכסי תוכנה (SAM Lead). תפקידך לבחון את קובץ הנתונים הגולמי ולזהות חריגות על פי חוקי הרישוי הנוקשים הבאים של הארגון:

1. מוצרים שאינם מיקרוסופט: שים לב למוצרים פרטניים כמו TreeSize, Canva, AMI וודא שהם מנוהלים כרישוי פרטני נפרד ולא נבלעים ברישוי הכללי.
2. סביבת GitPool: נתח האם השימוש הוא ככלי רוחבי או פרטני (קיימת מחלוקת ארגונית - שקף את הסטטוס והסיכונים).
3. רישוי שרתים ולקוחות בו זמנית (Concurrent): זהה שרתים ומערכות שבהם הרישוי מוגדר לפי כמות משתמשים מקסימלית בו-זמנית (ולא כלל ארגוני) ובדוק חריגות בכמות הלקוחות המחוברים בו"ז קבוע.
4. רכיבי תשתית ייעודיים: בדוק התאמה של רישיונות לבקרי הדפסה ותיבות מייל הצורכות רישוי פיזי או וירטואלי ברגע שהן מופעלות.
5. הגדרות וסוגי רישוי: לכל רישיון מזוהה, הגדר בבירור: מה מהות הרישוי? לכמה זמן? האם הוא משויך לפי משתמש (Per User) או לפי עמדה/מקור (Per Seat / Computer / מחשב מתחבר).
6. הבדל מערכות (מערכת סורקת VS הקצאה למשתמש): הפרד והדגש בין מערכות סרוקות (כמו סרוויס שסורק את מיקרוסופט ומציג כמה פנוי) לבין משתמש קצה פיזי שצריך לשייך לו רישיון באופן מנואל.
7. חוקי VIP (רשימת ה-50): השווה בין רשימת ה-VIP (50 משתמשים בכירים) לבין הרשימה הכללית. אם משתמש VIP מוגדר WITH רישוי כפול (למשל גם E3 וגם E5 במיקרוסופט), קבע האם מדובר בהקצאה זמנית או קבועה, והתרע על כפילויות.
8. מערכות ללא שיוך אוטומטי: סמן מוצרים שאין להם אופציה לצרף אנשים באופן אוטומטי (כמו Canva) הדורשים מעקב קפדני.

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

# ✅ 7. מנוע הפעלה ועיבוד בזמן אמת
st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
if st.button("⚡ הפעל ארכיטקטורת סוכנים אוטונומיים", type="primary"):
    
    try:
        # סוכן 1: Data Investigator
        analyst_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ANALYST
        )
        
        analyst_prompt = f"להלן נתוני הרישוי הארגוניים של החברה. בצע סריקה קפדנית והפק דוח חריגות ומקרי קצה מלא:\n\n{table_as_text}"
        
        with st.spinner("🤖 סוכן 1: Data Investigator סורק חריגות ומבני תשתית..."):
            res1 = analyst_model.generate_content(analyst_prompt)
            analyst_report = res1.text

        # סוכן 2: Strategic Architect
        architect_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ARCHITECT
        )
        
        architect_prompt = f"על בסיס דוח הממצאים המורכב ומקרי הקצה שמופו, גבש אסטרטגיית פעולה יישומית וסיכום מנהלים בכיר:\n\n{analyst_report}"
        
        with st.spinner("⚡ סוכן 2: Strategic Architect מייצר המלצות פיננסיות וסיכום בכירים..."):
            res2 = architect_model.generate_content(architect_prompt)
            architect_report = res2.text

        # 🌟 8. Workspace תוצרים מבוסס טאבים שטוחים
        st.markdown("<p style='color: #9ca3af; font-weight:600; margin: 30px 0 15px 0; font-size:0.9rem;'>💻 סביבת עבודה אסטרטגית</p>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🎯 ממצאי אנליסט הנתונים", "💎 תוכנית אסטרטגית וניסוח למנהלים"])
        
        with tab1:
            st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
            st.markdown(analyst_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab2:
            st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
            st.markdown(architect_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 📥 יצירת קובץ דוח מעוצב להורדה
        full_report = f"=========================================\nSAM CORE SYSTEM INTELLIGENCE REPORT\n=========================================\n\n[PART 1: DEEP ANALYTICS]\n\n{analyst_report}\n\n=========================================\n[PART 2: STRATEGIC ACTION PLAN]\n\n{architect_report}"
        b64 = base64.b64encode(full_report.encode('utf-8')).decode()
        
        st.markdown("---")
        st.markdown(
            f'<div style="text-align: left;"><a class="action-link" href="data:file/txt;base64,{b64}" download="SAM_Intelligence_Report.txt">📥 ייצוא קובץ נתונים משולב</a></div>',
            unsafe_allow_html=True
        )
        
    except Exception as api_error:
        st.error(f"❌ שגיאת רשת במערכת ה-AI: {api_error}")

st.markdown("</div>", unsafe_allow_html=True)
