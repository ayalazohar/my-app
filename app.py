import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. הגדרות מסך בסיסיות ועיצוב בעזרת CSS (שיפור נראות וקריאות בעברית)
st.set_page_config(
    page_title="SAM BI - מנוע אופטימיזציית רישוי", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# הזרקת עיצוב נקי למערכת (מראה ארגוני מודרני, יישור וריווחים)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stWidgetLabel"], .main {
        font-family: 'Assistant', sans-serif;
        text-align: right;
        direction: rtl;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. כותרות וסרגל צדדי סטנדרטי
st.title("📊 SAM BI · ניהול ותחקור נתוני רישוי")
st.subheader("טעינת מטריצות נתונים לעיבוד משולב, איתור חריגות תשתיות ומקרי קצה")
st.markdown("---")

with st.sidebar:
    st.header("🤖 SAM BI Engine")
    st.caption("מערכת ניתוח ובקרת משאבים מתקדמת")
    st.markdown("---")
    
    st.markdown("**⚙️ קונפיגורציית סריקה:**")
    st.info("""
    - **מנוע AI:** Gemini 2.5 Flash
    - **מודל עיבוד:** קבצי מבנה (Tabular)
    - **רמת ניתוח:** Edge-Case Deep Scan
    """)
    
    st.markdown("---")
    st.caption("פותח עבור צוות ניהול נכסי תוכנה ארגוניים © 2026")

# 3. אימות קונפיגורציית AI מול Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר במערכת. אנא הגדר אותו ב-Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# אתחול Session State לשמירת התוצאות (מונע היעלמות נתונים בלחיצה על כפתורים)
if "analyst_report" not in st.session_state:
    st.session_state.analyst_report = None
if "architect_report" not in st.session_state:
    st.session_state.architect_report = None
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

# 4. ממשק העלאת קבצים
uploaded_file = st.file_uploader("📂 העלה קובץ אקסל או CSV להפעלת מנגנון האופטימיזציה", type=["xlsx", "xls", "csv"])

# איפוס דוחות אם הועלה קובץ חדש
if uploaded_file is not None and uploaded_file.name != st.session_state.last_uploaded_file:
    st.session_state.analyst_report = None
    st.session_state.architect_report = None
    st.session_state.last_uploaded_file = uploaded_file.name

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.toast("🎯 זרם הנתונים נקלט וסונכרן בהצלחה", icon="🎯")
        
        # 5. חישוב והצגת מדדים (KPIs) ברכיבי Streamlit מובנים
        st.markdown("### 📈 תמונת מצב מטריצה גולמית")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="שורות מידע במטריצה", value=f"{df.shape[0]:,}")
        with col2:
            st.metric(label="פרמטרים ממופים (Columns)", value=df.shape[1])
        with col3:
            cost_cols = [c for c in df.columns if any(w in c.lower() for w in ['מחיר', 'עלות', 'cost', 'price'])]
            if cost_cols:
                total_cost = df[cost_cols[0]].sum()
                st.metric(label="חשיפה תקציבית נומינלית", value=f"₪{total_cost:,.0f}", delta="דורש טיוב", delta_color="inverse")
            else:
                st.metric(label="רמת רגישות הנתונים", value="מרובת קצוות")

        # הצגת טבלת הנתונים המובנית בתוך תיבה נגללת לנוחות
        with st.expander("👀 הצג תצוגה מקדימה של נתוני המקור הגולמיים (8 שורות ראשונות)", expanded=True):
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
    st.info("💡 המערכת ממתינה להעלאת קובץ הנתונים שלך כדי להתחיל בניתוח.")
    st.stop()

# 6. הנחיות המערכת עבור מודל ה-AI (נשאר ללא שינוי בלוגיקה)
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

# 7. מנוע הפעלה ותוצרים
st.markdown("### ⚙️ מנוע אופטימיזציה רב-סוכני")
run_analysis = st.button("🚀 הרץ עיבוד ואופטימיזציית סוכנים (AI Multi-Agent)", type="primary", use_container_width=True)

if run_analysis:
    try:
        # סוכן 1: Data Investigator
        analyst_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ANALYST
        )
        
        analyst_prompt = f"להלן נתוני הרישוי הארגוניים של החברה. בצע סריקה קפדנית והפק דוח חריגות ומקרי קצה מלא:\n\n{table_as_text}"
        
        # שימוש במנגנון סטטוס מתקדם במקום spinner פשוט
        with st.status("🔍 סוכן 1 (Data Investigator) מבצע סריקת עומק למטריצה...", expanded=True) as status:
            res1 = analyst_model.generate_content(analyst_prompt)
            st.session_state.analyst_report = res1.text
            status.update(label="✅ סוכן 1 סיים את המיפוי בהצלחה!", state="complete")

        # סוכן 2: Strategic Architect
        architect_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ARCHITECT
        )
        
        architect_prompt = f"על בסיס דוח הממצאים המורכב ומקרי הקצה שמופו, גבש אסטרטגיית פעולה יישומית וסיכום מנהלים בכיר:\n\n{st.session_state.analyst_report}"
        
        with st.status("🏗️ סוכן 2 (Strategic Architect) בונה המלצות אסטרטגיות ותוכנית חיסכון...", expanded=True) as status:
            res2 = architect_model.generate_content(architect_prompt)
            st.session_state.architect_report = res2.text
            status.update(label="✅ סוכן 2 סיים לגבש את תוכנית העבודה!", state="complete")
            
        st.balloons()

    except Exception as api_error:
        st.error(f"❌ שגיאת תקשורת ברשת ה-AI או פג תוקף המפתח: {api_error}")

# 8. הצגת תוצרים בטאבים מעוצבים (במידה וקיימים ב-Session State)
if st.session_state.analyst_report and st.session_state.architect_report:
    st.markdown("---")
    st.markdown("### 📋 תוצרי ניתוח ואופטימיזציה ארגונית")
    
    tab1, tab2 = st.tabs(["📊 דוח ממצאים וחריגות קצה (Analyst)", "🏢 תוכנית יישום וסיכום מנהלים (CTO)"])
    
    with tab1:
        st.markdown(st.session_state.analyst_report)
        
    with tab2:
        st.markdown(st.session_state.architect_report)
        
    # 9. יצירת אפשרות הורדה נוחה ומעוצבת בתחתית הדוח
    st.markdown("---")
    full_report = f"=========================================\nSAM BI ANALYTICS REPORT - 2026\n=========================================\n\n[PART 1: DATA ANALYTICS & EDGE CASES]\n\n{st.session_state.analyst_report}\n\n=========================================\n[PART 2: CTO STRATEGIC PLAN]\n\n{st.session_state.architect_report}"
    
    col_empty, col_download = st.columns([3, 1])
    with col_download:
        st.download_button(
            label="📥 ייצוא דוח משולב מלא (TXT)",
            data=full_report,
            file_name="SAM_BI_Executive_Report.txt",
            mime="text/plain",
            use_container_width=True
        )
