import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

# ✅ Page config
st.set_page_config(page_title="License Intelligence AI", layout="wide")

# 🎨 UI DESIGN
st.markdown("""
<style>
body {direction: RTL;}
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a);
    color: #e2e8f0;
}
.main-card {
    background: #111827;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}
.kpi {
    background: linear-gradient(135deg,#2563eb,#6366f1);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 18px;
}
button[kind="primary"] {
    background: linear-gradient(135deg,#22c55e,#16a34a);
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# 🔐 API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ חסר API")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 🧭 Sidebar
st.sidebar.title("⚙️ Control Panel")
uploaded_file = st.sidebar.file_uploader("📁 העלאת קובץ", type=["xlsx","csv","txt"])

# ✅ HERO SCREEN
if not uploaded_file:
    st.markdown("""
    <div style="text-align:center; padding:100px 20px;">
        <h1 style="font-size:48px;">🤖 License Intelligence AI</h1>
        <p style="font-size:20px; color:#9ca3af;">
        מערכת חכמה לניתוח רישוי ארגוני בזמן אמת
        </p>

        <div style="
            background:#111827;
            padding:40px;
            border-radius:16px;
            width:420px;
            margin:auto;
            margin-top:30px;
        ">
            <p style="font-size:18px;">📁 העלה קובץ כדי להתחיל</p>
            <p style="color:#6b7280;">Excel / CSV נתמכים</p>
        </div>

        <div style="margin-top:40px; color:#6b7280;">
            ⚡ ניתוח AI · 📉 חיסכון עלויות · 🔍 זיהוי כפילויות
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ✅ READ FILE
try:
    if uploaded_file.name.endswith("xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"שגיאה בקריאה: {e}")
    st.stop()

# ✅ HEADER
st.title("📊 License Intelligence Dashboard")

# ✅ KPI CARDS
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='kpi'>📦 רשומות<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

num_cols = df.select_dtypes(include="number").columns

if len(num_cols) > 0:
    col2.markdown(f"<div class='kpi'>💰 סה\"כ<br><h2>{int(df[num_cols[0]].sum())}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi'>📈 ממוצע<br><h2>{round(df[num_cols[0]].mean(),2)}</h2></div>", unsafe_allow_html=True)

# ✅ GRAPH
if len(num_cols) > 0:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 ניתוח גרפי")
    fig = px.bar(df, y=num_cols[0])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ✅ DATA TABLE
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.markdown("### 📋 נתונים")
st.dataframe(df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ✅ AI ANALYSIS
if st.button("🚀 הפעל ניתוח AI"):

    table_text = df.to_string(index=False)

    with st.spinner("🧠 מנתח נתונים..."):
        res1 = model.generate_content(
            f"נתח את הנתונים הארגוניים הבאים מצא בעיות רישוי:\n{table_text}"
        )
        analysis = res1.text

    with st.spinner("🛠️ מייצר תוכנית..."):
        res2 = model.generate_content(
            f"בהתבסס על זה תן המלצות אופרטיביות:\n{analysis}"
        )
        strategy = res2.text

    colA, colB = st.columns(2)

    with colA:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 ניתוח")
        st.markdown(analysis)
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("### 🚀 המלצות")
        st.markdown(strategy)
        st.markdown("</div>", unsafe_allow_html=True)
