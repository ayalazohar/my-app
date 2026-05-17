import streamlit as st
import pandas as pd
import os
import base64
from google import genai

# הגדרת עיצוב דף מודרני ב-Dark Mode
st.set_page_config(page_title="License Optimization AI", page_icon="🔍", layout="wide")

st.title("🔍 מערכת סוכני AI לאופטימיזציה וניהול רישוי ארגוני")
st.markdown("העלי קובץ אקסל של רישיונות לקבלת ניתוח עומק של חריגות, כפילויות VIP, ומודלים מורכבים.")

# 1. חיבור מאובטח ל-API - מושך את המפתח שהגדרת ב-Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("הזיני Gemini API Key לגיבוי:", type="password")

if not api_key:
    st.warning("🔑 אנא הגדירי את מפתח ה-API ב-Secrets של Streamlit או בסרגל הצד כדי להתחיל.")
    st.stop()

# אתחול ה-Client של גוגל
client = genai.Client(api_key=api_key)

# 2. רכיב העלאת קובץ אקסל בממשק
uploaded_file = st.file_uploader("בחרי קובץ אקסל (licenses.xlsx)", type=["xlsx", "xls"])

table_as_text = ""

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ קובץ האקסל האמיתי נטען בהצלחה! הנה הצצה לנתונים:")
        st.dataframe(df.head(10), use_container_width=True)
        table_as_text = df.to_markdown(index=False)
    except Exception as e:
        st.error(f"שגיאה בקריאת הקובץ: {e}")
else:
    st.info("💡 מציג נתוני סימולציה (Mock Data) המדמים את מקרי הקצה המורכבים של הארגון:")
    mock_data = {
        "מוצר/שירות": ["Microsoft 365 (VIP)", "TreeSize", "GitPull Environment", "בקרי הדפסה", "תיבות מייל משותפות", "Canva Pro", "מערכת סריקה (M365)"],
        "סוג/מודל רישוי": ["Per-User (E3+E5)", "פרטני (Per-Seat)", "Concurrent (שרתים)", "לפי מכשיר/תור", "צריכת רישיון אוטומטית", "פרטני (ידני)", "Service אוטומטי"],
        "כמות שנרכשה": [50, 5, 100, 10, 200, 10, 1],
        "בשימוש בפועל / סטטוס": ["48 משתמשים בכפל רישיונות קבוע", "מותקן ב-8 תחנות קצה פיזיות", "מקסימום 95 מחוברים בו-זמנית", "12 בקרי הדפסה פעילים", "205 תיבות פעילות (5 בחריגה)", "10 בשימוש, 15 בהמתנה", "מציג 15 רישיונות פנויים"],
        "עלות / הערות": ["כפל רישוי E3 ו-E5 ל-VIP", "רישוי על מקור/מחשב ספציפי", "כמות מקסימלית בו זמנית", "חריגת חומרה", "לוקח רישוי אוטומטית", "אין אופציה לצירוף אוטומטי", "סורק כמה פנוי בענן"]
    }
    df_mock = pd.DataFrame(mock_data)
    st.dataframe(df_mock, use_container_width=True)
    table_as_text = df_mock.to_markdown(index=False)

# 3. כפתור הרצת הסוכנים
if st.button("🚀 הפעל שרשרת סוכני AI לניתוח הרישוי"):
    
    # פרומפט מורכב הכוללים את כל מקרי הקצה שלך
    analyst_instructions = f"""
    אתה אנליסט בכיר לניהול נכסי תוכנה (SAM). נתח את הטבלה הבאה לפי מקרי קצה אלו:
    1. Per-User מול Per-Seat (כמו TreeSize - רישוי על מקור/מחשב שמתחבר).
    2. רישוי שרתים/לקוחות בו-זמנית (Concurrent כמו GitPull) - כמות מקסימלית בו זמנית ולא כלל ארגונית.
    3. בקרי הדפסה ותיבות מייל שלוקחות רישוי אוטומטית ברגע שלוקחים כל רישוי שהוא.
    4. פער בין מערכת סריקה אוטומטית (Service) למערכות ללא הצטרפות אוטומטית (קנבה) היוצרות תור המתנה.
    5. רשימות VIP המחזיקות בכפל רישיונות (גם E3 וגם E5) - קבע האם זמני או קבוע.
    
    הנתונים:
    {table_as_text}
    """
    
    with st.spinner("🧠 סוכן 1 (אנליסט חסכן) מנתח את מקרי הקצה ומחשב סיכונים..."):
        analyst_report = client.models.generate_content(model='gemini-2.5-flash', contents=analyst_instructions).text
        
    architect_instructions = f"""
    אתה ארכיטקט מערכות מידע ומנהל תפעול בכיר. בנה תוכנית עבודה על בסיס דוח האנליסט:
    1. פתרון לכפל רישוי VIP (ניקוי E3 ממשתמשי E5, קביעת זמני/קבוע).
    2. פתרון למערכות ללא הרשמה אוטומטית (קנבה) למניעת צוואר בקבוק.
    3. הסדרת רישוי תחנות (TreeSize) ותיבות מייל/בקרים.
    4. ניסוח הודעה רשמית, אסרטיבית ומקצועית להפצה לראשי הצוותים וקבוצת ה-VIP לגבי כפל הרישיונות והסדרתם.
    
    דוח האנליסט:
    {analyst_report}
    """
    
    with st.spinner("🛠️ סוכן 2 (ארכיטקט אסטרטגיה) מייצר תוכנית פעולה ונוסח הודעות..."):
        architect_report = client.models.generate_content(model='gemini-2.5-flash', contents=architect_instructions).text
        
    # 4. תצוגת התוצאות בממשק באמצעות טאבים מעוצבים
    tab1, tab2 = st.tabs(["📋 דוח אנליסט הרישוי (סוכן 1)", "🚀 תוכנית עבודה ותקשורת (סוכן 2)"])
    
    with tab1:
        st.subheader("ניתוח פערים, חריגות ובזבוז תקציבי")
        st.markdown(analyst_report)
        
    with tab2:
        st.subheader("תוכנית אסטרטגית וטיוטות הודעה לארגון")
        st.markdown(architect_report)
        
    # 5. שימוש ב-Base64 להורדה מאובטחת של הדוח הסופי כקובץ טקסט
    full_report = f"--- REPORT START ---\n\n== AGENT 1 REPORT ==\n\n{analyst_report}\n\n== AGENT 2 REPORT ==\n\n{architect_report}"
    b64 = base64.b64encode(full_report.encode('utf-8')).decode()
    href = f'<a href="data:file/text;base64,{b64}" download="Licensing_AI_Report.txt" style="text-decoration: none;"><button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">💾 הורדי דוח מלא כקובץ טקסט</button></a>'
    st.markdown(href, unsafe_content_type=True)
