import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ 1. הגדרות עמוד קריטיות למוצר אפליקטיבי
st.set_page_config(
    page_title="SAM OS Enterprise", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 2. ארכיטקטורת עיצוב פרימיום (Material Design Pro Workspace)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* רקע אפליקטיבי פרימיום בהיר ונקי */
    .stApp {
        background: #f3f4f6;
        color: #111827;
    }
    
    /* עיצוב סרגל הצד כמערכת ניווט של אפליקציה */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-left: 1px solid #e5e7eb !important;
        box-shadow: 2px 0 20px rgba(0,0,0,0.02) !important;
    }
    
    /* כרטיסי מוצר פרימיום חלקים */
    .product-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03);
    }
    
    /* פאנל אינדיקטורים מהיר */
    .product-badge {
        background: #f9fafb;
        border: 1px solid #f3f4f6;
        border-radius: 16px;
        padding: 16px 20px;
        text-align: right;
    }
    
    /* כפתור הפעלה רחב ומעוגל של אפליקציות ענן */
    button[kind="primary"] {
        background: #2563eb !important;
        border: none !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 0.85rem 2.5rem !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        width: 100%;
    }
    
    button[kind="primary"]:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* טאבים שטוחים של מוצרי SaaS */
    .stTabs [data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 700;
        color: #4b5563;
        background: transparent;
        padding: 12px 24px;
        transition: color 0.2s;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        border-bottom: 2px solid #2563eb !important;
    }
    
    /* מראה טבלאות נקי כמו מוצרי ניהול מתקדמים */
    [data-testid="stDataFrame"] {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    
    /* כפתור הורדה ייעודי */
    .product-download {
        display: inline-flex;
        align-items: center;
        padding: 10px 24px;
        background: #ffffff;
        color: #2563eb !important;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 700;
        font-size: 14px;
        border: 1px solid #d1d5db;
        transition: all 0.2s ease;
    }
    .product-download:hover {
        background: #f9fafb;
        border-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# 🏢 3. תפריט ניווט צידי (Sidebar App Navigation)
with st.sidebar:
    st.markdown("<h2 style='color:#111827; font-weight:800; margin-bottom: 5px;'>🛡️ SAM Core</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280; font-size:0.9rem; margin-top:0;'>פלטפורמת משילות רישוי ארגונית</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### ⚙️ מפרט מערכת")
    st.markdown("<div style='background:#f9fafb; padding:15px; border-radius:12px; border:1px solid #e5e7eb;'>"
                "<b>סטטוס:</b> <span style='color:#10b981;'>מחובר ומאובטח</span><br>"
                "<b>מנוע AI:</b> Gemini 2.5 Flash<br>"
                "<b>ארכיטקטורה:</b> Dual-Agent Pipeline"
                "</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<p style='color:#9ca3af; font-size:0.8rem; text-align:center;'>Enterprise Edition © 2026</p>", unsafe_allow_html=True)

# ⚡ 4. כותרת עבודה ראשית (Workspace Title)
st.markdown("""
<div style='background: #ffffff; border: 1px solid #e5e7eb; padding: 24px; border-radius: 20px; margin-bottom: 25px;'>
    <h1 style='font-weight: 800; font-size: 2rem; margin: 0; color: #111827;'>סביבת עבודה ואופטימיזציה</h1>
    <p style='color: #4b5563; font-size: 1rem; margin: 5px 0 0 0;'>העלי קובץ נתונים להרצת סוכני ה-AI לזיהוי חריגות, פערי תשתית ומקרי קצה</p>
</div>
""", unsafe_allow_html=True)

# ✅ 5. אימות קונפיגורציית AI מול Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר במערכת.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ 6. סביבת טעינת קבצים אפליקטיבית
uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.toast("🎯 זרם הנתונים נקלט וסונכרן במערכת", icon="✅")
        
        # 📊 פאנל אינדיקטורים מהיר (Product Dashboard Grid)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='product-badge'><span style='color:#4b5563; font-size:0.85rem;'>רשומות ממופות</span><br><b style='font-size:1.6rem; color:#111827;'>{df.shape[0]:,}</b></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='product-badge'><span style='color:#4b5563; font-size:0.85rem;'>עמודות מידע במטריצה</span><br><b style='font-size:1.6rem; color:#111827;'>{df.shape[1]}</b></div>", unsafe_allow_html=True)
        with col3:
            cost_cols = [c for c in df.columns if any(w in c.lower() for w in ['מחיר', 'עלות', 'cost', 'price'])]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.markdown(f"<div class='product-badge' style='background: #f0fdf4; border-color:#bbf7d0;'><span style='color:#166534; font-size:0.85rem;'>חשיפה תקציבית מזוהה</span><br><b style='font-size:1.6rem; color:#166534;'>₪{total_cost:,.0f}</b></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='product-badge' style='background: #fef2f2; border-color:#fca5a5;'><span style='color:#991b1b; font-size:0.85rem;'>רמת מורכבות סריקה</span><br><b style='font-size:1.6rem; color:#991b1b;'>מתקדם</b></div>", unsafe_allow_html=True)

        # הצגת גיליון הנתונים
        st.markdown("<div style='margin-top: 20px; margin-bottom: 25px;'>", unsafe_allow_html=True)
        st.dataframe(df.head(6), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # אופטימיזציית גודל נתונים לסוכנים
        if df.shape[0] > 500:
            table_as_text = df.head(500).to_string(index=False)
        else:
            table_as_text = df.to_string(index=False)

    except Exception as e:
        st.error(f"שגיאה בקריאת המקור: {e}")
        st.stop()
else:
    st.markdown("""
    <div style='text-align: center; padding: 50px 20px; border: 1px dashed #d1d5db; border-radius: 20px; background: #ffffff; margin-top: 15px;'>
        <span style='font-size: 2.2rem; color: #2563eb;'>📥</span>
        <h3 style='margin: 12px 0 4px 0; font-weight: 700; color: #111827; font-size: 1.15rem;'>הזנת מקור נתונים</h3>
        <p style='color: #4b5563; font-size: 0.95rem; margin: 0;'>גררי לכאן קובץ אקסל או CSV להפעלת מנגנון האופטימיזציה של הסוכנים</p>
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
if st.button("🚀 הפעל מערך סוכנים ואופטימיזציה", type="primary"):
    
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

        # 🌟 9. Workspace תוצרים מבוסס טאבים שטוחים
        st.markdown("<p style='color: #4b5563; font-weight:700; margin: 30px 0 15px 0; font-size:1rem;'>💻 פלטי סוכנים ומסמכים אסטרטגיים</p>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 דוח ממצאים וחריגות קצה", "📄 תוכנית יישום וסיכום מנהלים"])
        
        with tab1:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.markdown(analyst_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab2:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.markdown(architect_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 📥 יצירת קובץ דוח מעוצב להורדה
        full_report = f"=========================================\nSAM CORE SYSTEM EXECUTIVE REPORT\n=========================================\n\n[PART 1: ANALYTICS & EDGE CASES]\n\n{analyst_report}\n\n=========================================\n[PART 2: STRATEGIC ACTION PLAN]\n\n{architect_report}"
        b64 = base64.b64encode(full_report.encode('utf-8')).decode()
        
        st.markdown("---")
        st.markdown(
            f'<div style="text-align: left;"><a class="product-download" href="data:file/txt;base64,{b64}" download="SAM_Executive_Report.txt">📥 ייצוא דוח משולב</a></div>',
            unsafe_allow_html=True
        )
        
    except Exception as api_error:
        st.error(f"❌ שגיאת רשת במערכת ה-AI: {api_error}")

st.markdown("</div>", unsafe_allow_html=True)
