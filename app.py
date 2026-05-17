import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ 1. הגדרות עמוד מתקדמות (UI/UX)
st.set_page_config(
    page_title="SAM AI - Enterprise License Governance", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 2. עיצוב עתידני, קליל ומפוצץ (Next-Gen Cyberpunk UI)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stSidebarView"] {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
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
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2) !important;
        width: 100%;
    }
    
    button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.6) !important;
    }
    
    /* עיצוב הטאבים المרכזיים */
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        font-weight: 700;
        color: #64748b;
        padding: 10px 20px;
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
    }
    .download-cyber:hover {
        background: #06b6d4;
        color: #020617 !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ⚡ 3. כותרת ראשית חללית
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='font-weight: 800; font-size: 3rem; background: linear-gradient(90deg, #10b981, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        ⚡ SAM NEURAL INTELLIGENCE
    </h1>
    <p style='color: #94a3b8; font-size: 1.25rem; font-weight: 300; margin-top: -10px;'>
        ניהול ואופטימיזציית רישוי ארגוני מתקדמת כולל חוקיות מקרי קצה ומדיניות מורכבת
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ✅ 4. אימות מפתח API וקונפיגורציה
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ מפתח API (GEMINI_API_KEY) חסר ב-Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ 5. ממשק טעינת קבצים קליל ונקי
uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("🎯 הקובץ נקלט בהצלחה במערכת. המידע מוכן לעיבוד.")
        
        # 📊 כרטיסי מדדים (Metrics) מעוצבים
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
        
        # 🧠 לוגיקת אופטימיזציה לטקסט: מונע קריסה בקבצים גדולים
        if df.shape[0] > 500:
            st.warning("⚠️ הקובץ מכיל כמות שורות גדולה. המערכת תבצע מדגם מייצג של 500 השורות הראשונות לצורך ניתוח הסוכנים.")
            table_as_text = df.head(500).to_string(index=False)
        else:
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

# ✅ 6. הגדרת חוקי ה-Agent וכללי הקצה המורכבים ב-System Instructions
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

# ✅ 7. אזור הפעלת ארכיטקטורת הסוכנים
st.markdown("<div style='margin: 30px 0;'>", unsafe_allow_html=True)
if st.button("⚡ הזרק ניתוח ואופטימיזציה בזמן אמת", type="primary"):
    
    try:
        # סוכן 1: Data Investigator
        analyst_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ANALYST
        )
        
        analyst_prompt = f"להלן נתוני הרישוי הארגוניים של החברה. בצע סריקה קפדנית והפק דוח חריגות ומקרי קצה מלא:\n\n{table_as_text}"
        
        with st.spinner("🧠 סוכן 1 (Data Analyst) מפצח את חוקי הרישוי ומאתר חריגות מקרי קצה..."):
            res1 = analyst_model.generate_content(analyst_prompt)
            analyst_report = res1.text

        # סוכן 2: Strategic Architect
        architect_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION_ARCHITECT
        )
        
        architect_prompt = f"על בסיס דוח הממצאים המורכב ומקרי הקצה שמופו, גבש אסטרטגיית פעולה יישומית וסיכום מנהלים בכיר:\n\n{analyst_report}"
        
        with st.spinner("🚀 סוכן 2 (Strategic Architect) מייצר תוכנית אופטימיזציה פיננסית וסיכום מנהלים..."):
            res2 = architect_model.generate_content(architect_prompt)
            architect_report = res2.text

        # 🌟 הצגת התוצרים בטאבים עתידניים
        st.markdown("### 📊 תוצרי עיבוד הסוכנים")
        tab1, tab2 = st.tabs(["🎯 ממצאי אנליסט הנתונים (מקרי קצה וחריגות)", "💎 תוכנית אסטרטגית וניסוח למנהלים"])
        
        with tab1:
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            st.markdown(analyst_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with tab2:
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            st.markdown(architect_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # 📥 יצירת קובץ דוח מעוצב להורדה
        full_report = f"=========================================\nSAM NEURAL INTELLIGENCE REPORT - EDGE CASES INCLUDED\n=========================================\n\n[PART 1: DEEP EDGE-CASE ANALYTICS]\n\n{analyst_report}\n\n=========================================\n[PART 2: STRATEGIC ACTION PLAN & EXEC SUMMARY]\n\n{architect_report}"
        b64 = base64.b64encode(full_report.encode('utf-8')).decode()
        
        st.markdown("---")
        st.markdown(
            f'<div style="text-align: left;"><a class="download-cyber" href="data:file/txt;base64,{b64}" download="SAM_Intelligence_Report.txt">📥 ייצוא דוח מלא ומסוכם</a></div>',
            unsafe_allow_html=True
        )
        
    except Exception as api_error:
        st.error(f"❌ שגיאת תקשורת עם שרתי ה-AI: {api_error}")
        st.info("💡 מומלץ לוודא שמפתח ה-API תקין ורכיבי הרשת ב-Streamlit מעודכנים.")

st.markdown("</div>", unsafe_allow_html=True)
