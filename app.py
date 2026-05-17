import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ 1. הגדרות מסך רחב ותפריט צידי פתוח לטובת פריסת נתונים מקסימלית (BI View)
st.set_page_config(
    page_title="SAM BI — Analytics Engine", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 2. ארכיטקטורת עיצוב משודרגת (Premium UX/UI Dark Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* הגדרות גלובליות וכיווניות ימין לשמאל */
    html, body, [data-testid="stSidebarView"], .stApp {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
        background-color: #0b0f19 !important;
        color: #f8fafc;
    }
    
    /* עיצוב מחדש של אזור התוכן המרכזי */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px;
    }
    
    /* סרגל ניווט ימני מורחב, קשיח ומקצועי למניעת דחיסות */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-left: 1px solid #1e293b !important;
        border-right: none !important;
        min-width: 360px !important;
    }
    
    /* כותרת ראשית של הלוח האנליטי */
    .dashboard-header {
        text-align: center;
        margin-bottom: 50px;
        padding-top: 20px;
    }
    .dashboard-header h1 {
        font-size: 2.6rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }
    .dashboard-header p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin: 0;
        font-weight: 400;
    }

    /* קופסת העלאת הקבצים המעוצבת (Premium UX Drag & Drop Zone) */
    .custom-upload-zone {
        border: 2px dashed #334155;
        border-radius: 16px;
        background: #0f172a;
        padding: 80px 40px;
        text-align: center;
        margin-top: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .custom-upload-zone:hover {
        border-color: #3b82f6;
        background: #121b2e;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    .upload-icon {
        font-size: 3.5rem;
        color: #3b82f6;
        margin-bottom: 20px;
    }
    .upload-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }
    .upload-subtitle {
        color: #94a3b8;
        font-size: 1rem;
    }
    
    /* פריטי מידע מוגדלים, ברורים וקריאים בסרגל הצידי (High-Res Sidebar Items) */
    .sidebar-meta-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 12px;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 8px;
        border-radius: 10px;
        transition: background 0.2s ease;
    }
    .sidebar-meta-item:hover {
        background: #0f172a;
    }
    .sidebar-icon-wrapper {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .sidebar-badge {
        background: #1e293b;
        padding: 12px;
        border-radius: 12px;
        color: #3b82f6;
        font-size: 1.6rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border: 1px solid #334155;
    }
    .meta-text-title {
        color: #64748b; 
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .meta-text-value {
        color: #ffffff; 
        font-weight: 700; 
        font-size: 1.15rem;
    }
    
    /* קוביות מדדים וגרפים מרכזיים (BI Widgets) */
    .bi-widget {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* שכבת המגע השקופה של Streamlit מעל הציור המעוצב */
    [data-testid="stFileUploader"] {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        opacity: 0;
        cursor: pointer;
        z-index: 10;
    }
    .upload-container-relative {
        position: relative;
        width: 100%;
    }
    
    /* כפתור הפעלה טכני בולט (Primary Button) */
    button[kind="primary"] {
        background: #3b82f6 !important;
        border: 1px solid #2563eb !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 1rem 2.5rem !important;
        width: 100%;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
    }
    button[kind="primary"]:hover {
        background: #2563eb !important;
        box-shadow: 0 0 22px rgba(59, 130, 246, 0.45) !important;
        transform: translateY(-1px);
    }
    
    /* טאבים בסגנון פאנל דוחות מודרני */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
        color: #64748b;
        padding: 12px 24px;
    }
    .stTabs [aria-selected="true"] {
        color: #3b82f6 !important;
        border-bottom-color: #3b82f6 !important;
    }
    
    /* התאמת טבלאות הנתונים למראה נקי של גיליון אלקטרוני */
    [data-testid="stDataFrame"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 8px;
    }
    
    /* תחתית הסרגל הצידי */
    .sidebar-footer {
        position: absolute;
        bottom: 25px;
        right: 25px;
        color: #475569;
        font-size: 0.9rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 🏢 3. פאנל בקרה צידי משודרג ומרווח (System Control Sidebar)
with st.sidebar:
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; margin-top: 15px; padding: 0 10px;'>
        <div>
            <h2 style='color:#ffffff; font-weight:800; margin:0; font-size:2rem; letter-spacing: -0.5px;'>SAM BI</h2>
            <p style='color:#64748b; font-size:0.95rem; margin-top: 2px;'>Engine v2.5</p>
        </div>
        <div style='background: #1e293b; padding: 14px; border-radius: 14px; color: #3b82f6; font-size: 1.8rem; display: flex; align-items: center; border: 1px solid #334155;'>
            📈
        </div>
    </div>
    <p style='color:#94a3b8; font-size:1rem; font-weight:700; margin-bottom: 20px; padding-right: 10px;'>קונפיגורציית סריקה</p>
    """, unsafe_allow_html=True)
    
    # אלמנטים מוגדלים וקריאים לחלוטין מתוך ממשק ה-BI מהתמונה
    st.markdown("""
    <div class='sidebar-meta-item'>
        <div class='sidebar-icon-wrapper'>
            <span class='sidebar-badge'>🎛️</span>
            <div>
                <div class='meta-text-title'>מנוע AI</div>
                <div class='meta-text-value'>Gemini 2.5 Flash</div>
            </div>
        </div>
    </div>
    <div class='sidebar-meta-item'>
        <div class='sidebar-icon-wrapper'>
            <span class='sidebar-badge'>📦</span>
            <div>
                <div class='meta-text-title'>מודל עיבוד</div>
                <div class='meta-text-value'>Tabular Engine</div>
            </div>
        </div>
    </div>
    <div class='sidebar-meta-item'>
        <div class='sidebar-icon-wrapper'>
            <span class='sidebar-badge'>🛡️</span>
            <div>
                <div class='meta-text-title'>רמת ניתוח</div>
                <div class='meta-text-value'>Edge-Case Deep Scan</div>
            </div>
        </div>
    </div>
    <div class='sidebar-meta-item'>
        <div class='sidebar-icon-wrapper'>
            <span class='sidebar-badge'>⚡</span>
            <div>
                <div class='meta-text-title'>סוכנים פעילים</div>
                <div class='meta-text-value' style='font-family: "JetBrains Mono", monospace;'>(Analyst + CTO) 2</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-footer'>מערכת ניתוח ובקרת משאבים</div>", unsafe_allow_html=True)

# ⚡ 4. סרגל כותרת מרכזי עליון (Top Banner Workspace)
st.markdown("""
<div class='dashboard-header'>
    <h1>ניהול ותחקור נתוני רישוי</h1>
    <p>טעינת מטריצות נתונים לעיבוד משולב, איתור חריגות תשתיות ומקרי קצה</p>
</div>
""", unsafe_allow_html=True)

# ✅ 5. אימות קונפיגורציית AI מול Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר במערכת.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ 6. ממשק העלאת קבצים פרימיום קומפקטי ומעוצב
st.markdown("<div class='upload-container-relative'>", unsafe_allow_html=True)

st.markdown("""
<div class='custom-upload-zone'>
    <div class='upload-icon'>📤</div>
    <div class='upload-title'>העלה קובץ אקסל או CSV</div>
    <div class='upload-subtitle'>גרור ושחרר את הקובץ כאן או לחץ לניווט במערכת הקבצים</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.toast("🎯 זרם הנתונים נקלט וסונכרן בהצלחה", icon="✅")
        
        # 📊 לוח מחוונים ומדדי נתונים (KPI Summary Grid) ברכיבי Streamlit מובנים ומעוצבים
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="שורות מידע במטריצה", value=f"{df.shape[0]:,}")
        with col2:
            st.metric(label="פרמטרים ממופים (Columns)", value=df.shape[1])
        with col3:
            cost_cols = [c for c in df.columns if any(w in c.lower() for w in ['מחיר', 'עלות', 'cost', 'price'])]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.metric(label="חשיפה תקציבית נומינלית", value=f"₪{total_cost:,.0f}")
            else:
                st.metric(label="רמת רגישות הנתונים", value="מרובת קצוות")

        # הצגת גיליון הנתונים במראה אנליטי נקי
        st.markdown("<p style='color: #94a3b8; font-size:1.1rem; font-weight:600; margin-top:25px; margin-bottom:15px;'>📊 תצוגת נתוני מקור גולמיים</p>", unsafe_allow_html=True)
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
7. חוקי VIP (רשימת ה-50): השווה בין רשימת ה-VIP (50 משתמשים בכירים) לבין הרשימה הכללית. אם משתמש VIP מוגדר WITH רישוי כפול (למשל גם E3 וגם E5 במיקרוסופט), קבע האם מדובר בהקצאה זמנית או קבועה, והתרע על כפילויות.
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

# ⚡ 8. מנוע הפעלה וסביבת תוצרים
st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
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
        st.markdown("<p style='color: #94a3b8; font-weight:700; margin: 35px 0 15px 0; font-size:1.1rem;'>💻 דוחות וסיכומי מנהלים מבוססי AI</p>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 דוח ממצאים וחריגות קצה", "📋 תוכנית יישום וסיכום מנהלים"])
        
        with tab1:
            st.markdown("<div class='bi-widget'>", unsafe_allow_html=True)
            st.markdown(analyst_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab2:
            st.markdown("<div class='bi-widget'>", unsafe_allow_html=True)
            st.markdown(architect_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 📥 יצירת קובץ דוח מעוצב להורדה באמצעות כפתור מובנה
        full_report = f"=========================================\nSAM BI ANALYTICS REPORT\n=========================================\n\n[PART 1: DATA ANALYTICS & EDGE CASES]\n\n{analyst_report}\n\n=========================================\n[PART 2: CTO STRATEGIC PLAN]\n\n{architect_report}"
        
        st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
        st.download_button(
            label="📥 ייצוא דוח משולב (TXT)",
            data=full_report,
            file_name="SAM_BI_Executive_Report.txt",
            mime="text/plain"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    except Exception as api_error:
        st.error(f"❌ שגיאת תקשורת ברשת ה-AI: {api_error}")

st.markdown("</div>", unsafe_allow_html=True)
