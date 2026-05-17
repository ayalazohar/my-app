import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ 1. הגדרות מערכת וארכיטקטורת עמוד
st.set_page_config(
    page_title="SAM Workspace", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 2. ממשק עיצוב גוגל יוקרתי ובהיר (Material Design 3 Evolution)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* רקע גוגל נקי ויוקרתי */
    .stApp {
        background: #f8f9fa;
        color: #1f1f1f;
    }
    
    /* כרטיסי Material Design צפים ורכים */
    .google-card {
        background: #ffffff;
        border: 1px solid #e0e3e7;
        border-radius: 28px;
        padding: 30px;
        margin-bottom: 24px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .google-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    }
    
    /* תיבות מדדים קלילות (Google Material Chips) */
    .google-indicator {
        background: #f0f4f9;
        border-radius: 20px;
        padding: 20px;
        text-align: right;
        border: 1px solid transparent;
    }
    
    /* כפתור הפעלה בעיצוב כפתורי הפרימיום של גוגל */
    button[kind="primary"] {
        background: #1a73e8 !important;
        border: none !important;
        border-radius: 100px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 0.9rem 2.5rem !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 1px 3px rgba(26,115,232,0.4), 0 4px 10px rgba(26,115,232,0.2) !important;
        width: 100%;
    }
    
    button[kind="primary"]:hover {
        background: #1557b0 !important;
        box-shadow: 0 1px 3px rgba(21,87,176,0.4), 0 8px 20px rgba(21,87,176,0.3) !important;
        transform: translateY(-1px);
    }
    
    /* טאבים בסגנון Google Cloud / Material Tabs */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
        color: #5f6368;
        background: transparent;
        padding: 12px 24px;
        border-bottom: 3px solid transparent;
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #1a73e8;
    }
    .stTabs [aria-selected="true"] {
        color: #1a73e8 !important;
        border-bottom: 3px solid #1a73e8 !important;
    }
    
    /* עיצוב רכיבי האקסל כמו Google Sheets */
    [data-testid="stDataFrame"] {
        background: #ffffff !important;
        border: 1px solid #e0e3e7 !important;
        border-radius: 16px !important;
        overflow: hidden;
    }
    
    /* כפתור הורדה מעוצב ככפתור גוגל משני (Outline Button) */
    .google-download {
        display: inline-flex;
        align-items: center;
        padding: 12px 28px;
        background: #ffffff;
        color: #1a73e8 !important;
        text-decoration: none;
        border-radius: 100px;
        font-weight: 700;
        font-size: 15px;
        border: 1px solid #dadce0;
        transition: all 0.2s ease;
    }
    .google-download:hover {
        background: #f8fafd;
        border-color: #1a73e8;
    }
</style>
""", unsafe_allow_html=True)

# ⚡ 3. כותרת עליונה בסגנון Google Workspace Cloud
st.markdown("""
<div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e0e3e7; padding-bottom: 25px; margin-bottom: 35px;'>
    <div style='display: flex; align-items: center; gap: 15px;'>
        <div style='background: #e8f0fe; padding: 12px; border-radius: 16px; display: flex; align-items: center; justify-content: center;'>
            <span style='font-size: 2rem;'>📊</span>
        </div>
        <div>
            <h1 style='font-weight: 700; font-size: 2.2rem; margin: 0; color: #1f1f1f; letter-spacing: -0.5px;'>SAM Workspace</h1>
            <p style='color: #5f6368; font-size: 1.05rem; margin: 4px 0 0 0;'>ניהול חוקיות רישוי ומקרי קצה בסביבת עבודה חכמה מבוססת סוכנים</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ 4. אימות קונפיגורציית AI מול Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר במערכת.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ 5. סביבת טעינת קבצים אלגנטית
uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.toast("🎯 קובץ הנתונים סונכרן בהצלחה", icon="✅")
        
        # 📊 פאנל אינדיקטורים מהיר (Google Style Dashboard)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='google-indicator'><span style='color:#5f6368; font-size:0.9rem;'>שורות שזוהו</span><br><b style='font-size:1.8rem; color:#1f1f1f;'>{df.shape[0]:,}</b></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='google-indicator'><span style='color:#5f6368; font-size:0.9rem;'>מאפייני מערכת</span><br><b style='font-size:1.8rem; color:#1f1f1f;'>{df.shape[1]}</b></div>", unsafe_allow_html=True)
        with col3:
            cost_cols = [c for c in df.columns if any(w in c.lower() for w in ['מחיר', 'עלות', 'cost', 'price'])]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.markdown(f"<div class='google-indicator' style='background: #e6f4ea;'><span style='color:#137333; font-size:0.9rem;'>היקף פיננסי ממופה</span><br><b style='font-size:1.8rem; color:#137333;'>₪{total_cost:,.0f}</b></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='google-indicator' style='background: #fce8e6;'><span style='color:#c5221f; font-size:0.9rem;'>מצב ניתוח</span><br><b style='font-size:1.8rem; color:#c5221f;'>נדרש סריקה</b></div>", unsafe_allow_html=True)

        # הצגת גיליון הנתונים במראה אקסל נקי ומקצועי
        st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
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
    <div style='text-align: center; padding: 60px 20px; border: 1px dashed #dadce0; border-radius: 24px; background: #ffffff; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-top: 15px;'>
        <span style='font-size: 2.5rem; color: #1a73e8;'>📥</span>
        <h3 style='margin: 15px 0 5px 0; font-weight: 600; color: #1f1f1f; font-size: 1.2rem;'>העלאת קובץ נתונים</h3>
        <p style='color: #5f6368; font-size: 0.95rem; margin: 0;'>בחרי או גררי קובץ Excel או CSV כדי להתחיל בעבודה עם ה-AI</p>
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
7. חוקי VIP (רשימת ה-50): השווה בין רשימת ה-VIP (50 משתמשים בכירים) לבין הרשימה הכללית. אם משתמש VIP מוגדר עם רישוי כפול (למשל גם E3 וגם E5 במיקרוסופט), קבע האם מדובר בהקצאה זמנית או קבועה, והתרע על כפילויות.
8. מערכות ללא שיוך אוטומטי: סמן מוצרים שאין להם אופציה לצרף אנשים באופן אוטומטי (כמו Canva) הדורשים מעקב קפדני.

הצג את הממצאים שלך בעברית מקצועית, תוך שימוש בטבלאות Markdown מסודרות לחריגות ובולטים ברורים.
"""

SYSTEM_INSTRUCTION_ARCHITECT = """
אתה ארכיטקט מערכות מידע ומנהל טכנולוגיות ראשי (CTO). תפקידך לקבל את דוח הממצאים וחריגות מקרי הקצה של האנליסט ולהפוך אותו לתוכנית עבודה קונקרטית, המלצות לחיסכון, וניסוח רשמי להנהלה.

עליך לבנות:
1. תוכנית אסטרטגית ליישוב המחלוקות (כגון מודל הרישוי של GitPool, וכפילויות ה-VIP של E3+E5).
2. המלצות מעשיות להתמודדות WITH מערכות שאינן תומכות באוטומציה (כמו Canva, רישוי לבקרי הדפסה ותיבות מייל).
3. פתרונות ייעודיים לניהול רישיונות לפי עמדה (Per Seat) לעומת משתמש (Per User).
4. ניסוח הודעה רשמית, חדה ומקצועית המיועדת למנהלים בכירים (Executive Summary) המסכמת את הסיכונים, החיסכון הכלכלי הצפוי והצעדים הבאים.

ענה בעברית עסקית רהוטה ונקייה.
"""

# ✅ 7. מנוע הפעלה ועיבוד בזמן אמת
st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
if st.button("🚀 הפעל ניתוח ואופטימיזציה חכמה", type="primary"):
    
    try:
        # סוכן 1: Data Investigator
        analyst_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ANALYST
        )
        
        analyst_prompt = f"להלן נתוני הרישוי הארגוניים של החברה. בצע סריקה קפדנית והפק דוח חריגות ומקרי קצה מלא:\n\n{table_as_text}"
        
        with st.spinner("🧠 סוכן האנליסט מעבד נתוני מקרי קצה ותשתיות..."):
            res1 = analyst_model.generate_content(analyst_prompt)
            analyst_report = res1.text

        # סוכן 2: Strategic Architect
        architect_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ARCHITECT
        )
        
        architect_prompt = f"על בסיס דוח הממצאים המורכב ומקרי הקצה שמופו, גבש אסטרטגיית פעולה יישומית וסיכום מנהלים בכיר:\n\n{analyst_report}"
        
        with st.spinner("⚙️ סוכן הארכיטקט מגבש המלצות פיננסיות וסיכום בכירים..."):
            res2 = architect_model.generate_content(architect_prompt)
            architect_report = res2.text

        # 🌟 8. Workspace תוצרים מבוסס טאבים של גוגל
        st.markdown("<p style='color: #5f6368; font-weight:700; margin: 35px 0 15px 0; font-size:1rem;'>💻 סביבת עבודה ואסטרטגיה</p>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 ממצאי אנליסט הנתונים", "📄 תוכנית אסטרטגית וניסוח למנהלים"])
        
        with tab1:
            st.markdown("<div class='google-card'>", unsafe_allow_html=True)
            st.markdown(analyst_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab2:
            st.markdown("<div class='google-card'>", unsafe_allow_html=True)
            st.markdown(architect_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 📥 יצירת קובץ דוח מעוצב להורדה
        full_report = f"=========================================\nSAM WORKSPACE SYSTEM REPORT\n=========================================\n\n[PART 1: ANALYTICS]\n\n{analyst_report}\n\n=========================================\n[PART 2: STRATEGIC ACTION PLAN]\n\n{architect_report}"
        b64 = base64.b64encode(full_report.encode('utf-8')).decode()
        
        st.markdown("---")
        st.markdown(
            f'<div style="text-align: left;"><a class="google-download" href="data:file/txt;base64,{b64}" download="SAM_Workspace_Report.txt">📥 ייצוא דוח משולב</a></div>',
            unsafe_allow_html=True
        )
        
    except Exception as api_error:
        st.error(f"❌ שגיאת רשת במערכת ה-AI: {api_error}")

st.markdown("</div>", unsafe_allow_html=True)
