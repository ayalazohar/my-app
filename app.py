import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ 1. הגדרות מסך רחב לטובת פריסת נתונים מקסימלית (BI View)
st.set_page_config(
    page_title="SAM BI — Analytics Engine", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 2. ארכיטקטורת עיצוב של לוח מחוונים אנליטי (Data-Dense Dashboard Style)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Assistant:wght@300;400;600;700;800&display=swap');
    
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* רקע כהה הנדסי מעודן למניעת עייפות עין */
    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }
    
    /* סרגל ניווט שמאלי קשיח ומקצועי */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-left: 1px solid #1e293b !important;
    }
    
    /* קוביות מדדים וגרפים (BI Widgets) */
    .bi-widget {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* כותרות קטנות וממוקדות למדדים */
    .widget-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* תצוגת מספרים הנדסית */
    .widget-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 5px;
    }
    
    /* כפתור הפעלה טכני בולט */
    button[kind="primary"] {
        background: #3b82f6 !important;
        border: 1px solid #2563eb !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }
    
    button[kind="primary"]:hover {
        background: #2563eb !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* טאבים בסגנון פאנל דוחות */
    .stTabs [data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
        color: #64748b;
        padding: 10px 20px;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #3b82f6 !important;
        border-bottom: 2px solid #3b82f6 !important;
    }
    
    /* התאמת טבלאות הנתונים למראה נקי של גיליון אלקטרוני */
    [data-testid="stDataFrame"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    /* כפתור ייצוא דוח שטוח ומקצועי */
    .bi-export-btn {
        display: inline-flex;
        align-items: center;
        padding: 10px 24px;
        background: #0f172a;
        color: #3b82f6 !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
        border: 1px solid #334155;
        transition: all 0.2s ease;
    }
    .bi-export-btn:hover {
        background: #1e293b;
        border-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# 🏢 3. פאנל בקרה צידי (System Control Sidebar)
with st.sidebar:
    st.markdown("<h2 style='color:#ffffff; font-weight:800; margin-bottom: 5px; font-size:1.4rem;'>📊 SAM BI Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:0.85rem; margin-top:0;'>מערכת ניתוח ובקרת משאבים</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem; font-weight:600;'>קונפיגורציית סריקה</p>", unsafe_allow_html=True)
    st.markdown("<div style='background:#1e293b; padding:12px; border-radius:8px; border:1px solid #334155; font-size:0.85rem; color:#cbd5e1;'>"
                "• <b>מנוע AI:</b> Gemini 2.5 Flash<br>"
                "• <b>מודל עיבוד:</b> קבצי מבנה (Tabular)<br>"
                "• <b>רמת ניתוח:</b> Edge-Case Deep Scan"
                "</div>", unsafe_allow_html=True)
    st.markdown("---")

# ⚡ 4. סרגל כותרת עליון (Top Banner Workspace)
st.markdown("""
<div style='background: #1e293b; border: 1px solid #334155; padding: 20px; border-radius: 12px; margin-bottom: 25px;'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 style='font-weight: 700; font-size: 1.8rem; margin: 0; color: #ffffff;'>ניהול ותחקור נתוני רישוי</h1>
            <p style='color: #94a3b8; font-size: 0.95rem; margin: 4px 0 0 0;'>טעינת מטריצות נתונים לעיבוד משולב, איתור חריגות תשתיות ומקרי קצה</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ 5. אימות קונפיגורציית AI מול Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר במערכת.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ 6. ממשק העלאת קבצים קומפקטי
uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.toast("🎯 זרם הנתונים נקלט וסונכרן בהצלחה", icon="✅")
        
        # 📊 לוח מחוונים ומדדי נתונים (KPI Summary Grid)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='bi-widget'><div class='widget-label'>שורות מידע במטריצה</div><div class='widget-value'>{df.shape[0]:,}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='bi-widget'><div class='widget-label'>פרמטרים ממופים (Columns)</div><div class='widget-value'>{df.shape[1]}</div></div>", unsafe_allow_html=True)
        with col3:
            cost_cols = [c for c in df.columns if any(w in c.lower() for w in ['מחיר', 'עלות', 'cost', 'price'])]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.markdown(f"<div class='bi-widget' style='border-color: #22c55e;'><div class='widget-label' style='color:#22c55e;'>חשיפה תקציבית נומינלית</div><div class='widget-value' style='color:#22c55e;'>₪{total_cost:,.0f}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='bi-widget' style='border-color: #eab308;'><div class='widget-label' style='color:#eab308;'>רמת רגישות הנתונים</div><div class='widget-value' style='color:#eab308;'>מרובת קצוות</div></div>", unsafe_allow_html=True)

        # הצגת גיליון הנתונים במראה אנליטי נקי
        st.markdown("<p style='color: #94a3b8; font-size:0.9rem; font-weight:600; margin-bottom:10px;'>📊 תצוגת נתוני מקור גולמיים</p>", unsafe_allow_html=True)
        st.dataframe(df.head(8), use_container_width=True)
        
        # אופטימיזציית נפח טקסט עבור הסוכנים
        if df.shape[0] > 500:
            table_as_text = df.head(500).to_string(index=False)
        else:
            table_as_text = df.to_string(index=False)

    except Exception as e:
        st.error(f"שגיאה בקריאת המקור: {e}")
        st.stop()
else:
    st.markdown("""
    <div style='text-align: center; padding: 45px 20px; border: 1px dashed #334155; border-radius: 12px; background: #1e293b; margin-top: 15px;'>
        <span style='font-size: 2rem; color: #3b82f6;'>📥</span>
        <h3 style='margin: 10px 0 5px 0; font-weight: 700; color: #ffffff; font-size: 1.1rem;'>הזנת קובץ נתונים</h3>
        <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>גררי לכאן קובץ אקסל או CSV להפעלת מנגנון האופטימיזציה של הסוכנים</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# 🧠 7. הגדרות חוקיות ומקרי קצה עבור הסוכנים האוטונומיים
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
2. המלצות מעשיות להתמודדות עם מערכות שאינן תומכות באוטומציה (כמו Canva, רישוי לבקרי הדפסה ותיבות מייל).
3. פתרונות ייעודיים לניהול רישיונות לפי עמדה (Per Seat) לעומת משתמש (Per User).
4. ניסוח הודעה רשמית, חדה ומקצועית המיועדת למנהלים בכירים (Executive Summary) המסכמת את הסיכונים, החיסכון הכלכלי הצפוי והצעדים הבאים.

ענה בעברית עסקית רהוטה ונקייה.
"""

# ✅ 8. מנוע הפעלה וסביבת תוצרים
st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
if st.button("🚀 הרץ עיבוד ואופטימיזציית סוכנים", type="primary"):
    
    try:
        # סוכן 1: Data Investigator
        analyst_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ANALYST
        )
        
        analyst_prompt = f"להלן נתוני הרישוי הארגוניים של החברה. בצע סריקה קפדנית והפק דוח חריגות ומקרי קצה מלא:\n\n{table_as_text}"
        
        with st.spinner("🤖 סוכן 1 (Data Investigator) מעבד נתוני מטריצה..."):
            res1 = analyst_model.generate_content(analyst_prompt)
            analyst_report = res1.text

        # סוכן 2: Strategic Architect
        architect_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ARCHITECT
        )
        
        architect_prompt = f"על בסיס דוח הממצאים המורכב ומקרי הקצה שמופו, גבש אסטרטגיית פעולה יישומית וסיכום מנהלים בכיר:\n\n{analyst_report}"
        
        with st.spinner("⚙️ סוכן 2 (Strategic Architect) גוזר המלצות אופטימיזציה..."):
            res2 = architect_model.generate_content(architect_prompt)
            architect_report = res2.text

        # 🌟 9. פלט דוחות וטאבים בסגנון פאנל אנליטי
        st.markdown("<p style='color: #94a3b8; font-weight:700; margin: 30px 0 15px 0; font-size:0.95rem;'>💻 דוחות וסיכומי מנהלים מבוססי AI</p>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 דוח ממצאים וחריגות קצה", "📋 תוכנית יישום וסיכום מנהלים"])
        
        with tab1:
            st.markdown("<div class='bi-widget'>", unsafe_allow_html=True)
            st.markdown(analyst_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab2:
            st.markdown("<div class='bi-widget'>", unsafe_allow_html=True)
            st.markdown(architect_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 📥 יצירת קובץ דוח מעוצב להורדה
        full_report = f"=========================================\nSAM BI ANALYTICS REPORT\n=========================================\n\n[PART 1: DATA ANALYTICS & EDGE CASES]\n\n{analyst_report}\n\n=========================================\n[PART 2: CTO STRATEGIC PLAN]\n\n{architect_report}"
        b64 = base64.b64encode(full_report.encode('utf-8')).decode()
        
        st.markdown("---")
        st.markdown(
            f'<div style="text-align: left;"><a class="bi-export-btn" href="data:file/txt;base64,{b64}" download="SAM_BI_Executive_Report.txt">📥 ייצוא דוח משולב (TXT)</a></div>',
            unsafe_allow_html=True
        )
        
    except Exception as api_error:
        st.error(f"❌ שגיאת תקשורת ברשת ה-AI: {api_error}")

st.markdown("</div>", unsafe_allow_html=True)
