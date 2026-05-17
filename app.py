import streamlit as st
import pandas as pd
import base64
import google.generativeai as genai

# ✅ 1. הגדרות מסך רחב ותפריט צידי פתוח
st.set_page_config(
    page_title="SAM BI — Analytics Engine", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 2. ארכיטקטורת העיצוב המדויקת מהצילום (Dark BI Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&display=swap');
    
    /* הגדרות גלובליות וכיווניות ימין לשמאל */
    html, body, [data-testid="stSidebarView"], .stApp {
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
        background-color: #0b0f19 !important; /* רקע כהה עמוק כמו בצילום */
        color: #f8fafc;
    }
    
    /* עיצוב מחדש של אזור התוכן המרכזי */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* סרגל ניווט ימני (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-left: 1px solid #1e293b !important;
        border-right: none !important;
    }
    
    /* כותרת ראשית של הלוח */
    .dashboard-header {
        text-align: center;
        margin-bottom: 40px;
        padding-top: 10px;
    }
    .dashboard-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }
    .dashboard-header p {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }

    /* קופסת העלאת הקבצים המעוצבת (Drag & Drop Zone) */
    .custom-upload-zone {
        border: 2px dashed #1e293b;
        border-radius: 12px;
        background: #0f172a;
        padding: 60px 20px;
        text-align: center;
        margin-top: 20px;
        transition: border-color 0.2s ease;
    }
    .custom-upload-zone:hover {
        border-color: #3b82f6;
    }
    .upload-icon {
        font-size: 2.5rem;
        color: #64748b;
        margin-bottom: 15px;
    }
    .upload-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }
    .upload-subtitle {
        color: #64748b;
        font-size: 0.95rem;
    }
    
    /* פריטי מידע ונתונים בסרגל הצידי (Sidebar Meta Items) */
    .sidebar-meta-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #1e293b;
    }
    .sidebar-meta-label {
        color: #64748b;
        font-size: 0.9rem;
    }
    .sidebar-meta-value {
        color: #ffffff;
        font-weight: 700;
        font-size: 1rem;
    }
    .sidebar-icon-wrapper {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sidebar-badge {
        background: #1e293b;
        padding: 6px;
        border-radius: 8px;
        color: #3b82f6;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    
    /* החבאת התיבה המקורית של Streamlit והשארת כפתור הפעולה שקוף מעל הציור שלנו */
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
    
    /* כפתור הפעלה ראשי (Primary Button) */
    button[kind="primary"] {
        background: #3b82f6 !important;
        border: none !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 0.75rem 2rem !important;
        width: 100%;
    }
    
    /* תחתית הסרגל הצידי */
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        right: 20px;
        color: #475569;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# 🏢 3. פאנל בקרה צידי (System Control Sidebar) - לפי התמונה בדיוק
with st.sidebar:
    # כותרת עליונה בסיידבר עם האייקון הספציפי
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; margin-top: 10px;'>
        <div>
            <h2 style='color:#ffffff; font-weight:800; margin:0; font-size:1.6rem;'>SAM BI</h2>
            <p style='color:#64748b; font-size:0.85rem; margin:0;'>Engine v2.5</p>
        </div>
        <div style='background: #1e293b; padding: 10px; border-radius: 12px; color: #3b82f6; font-size: 1.5rem; display: flex; align-items: center;'>
            📈
        </div>
    </div>
    <p style='color:#64748b; font-size:0.9rem; font-weight:600; margin-bottom: 15px;'>קונפיגורציית סריקה</p>
    """, unsafe_allow_html=True)
    
    # פריטי המטא דאטה של הקונפיגורציה עם האייקונים מהצילום
    st.markdown("""
    <div class='sidebar-meta-item'>
        <div class='sidebar-icon-wrapper'>
            <span class='sidebar-badge'>🎛️</span>
            <div>
                <div style='color: #64748b; font-size: 0.8rem;'>מנוע AI</div>
                <div style='color: #ffffff; font-weight: 700; font-size: 0.95rem;'>Gemini 2.5 Flash</div>
            </div>
        </div>
    </div>
    <div class='sidebar-meta-item'>
        <div class='sidebar-icon-wrapper'>
            <span class='sidebar-badge'>📦</span>
            <div>
                <div style='color: #64748b; font-size: 0.8rem;'>מודל עיבוד</div>
                <div style='color: #ffffff; font-weight: 700; font-size: 0.95rem;'>Tabular</div>
            </div>
        </div>
    </div>
    <div class='sidebar-meta-item'>
        <div class='sidebar-icon-wrapper'>
            <span class='sidebar-badge'>🛡️</span>
            <div>
                <div style='color: #64748b; font-size: 0.8rem;'>רמת ניתוח</div>
                <div style='color: #ffffff; font-weight: 700; font-size: 0.95rem;'>Edge-Case Deep Scan</div>
            </div>
        </div>
    </div>
    <div class='sidebar-meta-item'>
        <div class='sidebar-icon-wrapper'>
            <span class='sidebar-badge'>⚡</span>
            <div>
                <div style='color: #64748b; font-size: 0.8rem;'>סוכנים פעילים</div>
                <div style='color: #ffffff; font-weight: 700; font-size: 0.95rem;'>(Analyst + CTO) 2</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # טקסט תחתית קטן קבוע בסיידבר
    st.markdown("<div class='sidebar-footer'>מערכת ניתוח ובקרת משאבים</div>", unsafe_allow_html=True)

# ⚡ 4. סרגל כותרת מרכזי עליון
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

# ✅ 6. ממשק העלאת קבצים מעוצב ומותאם אישית (Custom File Uploader UI Layer)
# אנחנו עוטפים את הכל בתוך דיב יחסי כדי שרכיב ההעלאה השקוף של ה-Streamlit ישב בדיוק מעל העיצוב הויזואלי
st.markdown("<div class='upload-container-relative'>", unsafe_allow_html=True)

# כאן מוזרק ה-UI האלטרנטיבי שנראה כמו בצילום מסך
st.markdown("""
<div class='custom-upload-zone'>
    <div class='upload-icon'>📤</div>
    <div class='upload-title'>העלה קובץ אקסל או CSV</div>
    <div class='upload-subtitle'>גרור ושחרר או לחץ לבחירת קובץ</div>
</div>
""", unsafe_allow_html=True)

# זה הרכיב האמיתי של Streamlit שתופס את הלחיצות והגרירות אך מוסתר ויזואלית באמצעות CSS opacity: 0
uploaded_file = st.file_uploader("", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# 🧠 7. הלוגיקה העסקית והוראות הסוכנים (נשארות פעילות ברקע)
SYSTEM_INSTRUCTION_ANALYST = "..."
SYSTEM_INSTRUCTION_ARCHITECT = "..."

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.toast("🎯 זרם הנתונים נקלט וסונכרן בהצלחה", icon="✅")
        
        # הדפסת הנתונים והמשך המנוע לאחר טעינת הקובץ בהצלחה...
        st.write("### תצוגת נתוני מקור גולמיים")
        st.dataframe(df.head(8), use_container_width=True)

    except Exception as e:
        st.error(f"שגיאה בקריאת המקור: {e}")
