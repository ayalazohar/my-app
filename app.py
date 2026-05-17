import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# ✅ CONFIG
st.set_page_config(page_title="License AI", layout="wide")

# ✅ DESIGN SYSTEM (מודרני נקי)
st.markdown("""
<style>
body {direction: RTL;}
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a);
    color:#e5e7eb;
}

/* HERO */
.hero {
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    height:85vh;
    text-align:center;
}

.hero-title {
    font-size:56px;
    font-weight:800;
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-sub {
    font-size:18px;
    color:#9ca3af;
    margin-top:10px;
    margin-bottom:30px;
}

/* CARD */
.card {
    background:#111827;
    padding:20px;
    border-radius:14px;
    box-shadow:0 10px 30px rgba(0,0,0,0.4);
}

/* KPI */
.kpi {
    background: linear-gradient(135deg,#2563eb,#6366f1);
    padding:20px;
    border-radius:12px;
    text-align:center;
    color:white;
}

/* BUTTON */
button[kind="primary"] {
    background: linear-gradient(135deg,#22c55e,#16a34a);
    border-radius:10px;
    height:50px;
    font-size:16px;
}
</style>
""", unsafe_allow_html=True)

# ✅ API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ אין API KEY")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ HERO + UPLOAD במרכז
uploaded_file = st.file_uploader("", type=["xlsx","csv","txt"])

if not uploaded_file:

    st.markdown("""
    <div class="hero">
        <div class="hero-title">License Intelligence</div>

        <div class="hero-sub">
        מערכת AI לניהול ואופטימיזציה של רישוי ארגוני
        </div>

        <div class="card" style="width:350px;">
            📁 גרור קובץ או לחץ להעלאה
            <br><br>
            <small style="color:#9ca3af;">
            Excel / CSV נתמכים
            </small>
        </div>

        <div style="margin-top:30px; color:#6b7280;">
        🔍 זיהוי כפילויות · 📉 חיסכון · ⚡ ניתוח מהיר
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ✅ LOAD DATA
try:
    if uploaded_file.name.endswith("xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"שגיאה בקריאת קובץ: {e}")
    st.stop()

# ✅ HEADER
st.markdown("## 📊 Dashboard")

# ✅ KPI
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='kpi'>📦 רשומות<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

num_cols = df.select_dtypes(include='number').columns

if len(num_cols) > 0:
    col2.markdown(f"<div class='kpi'>💰 סה\"כ<br><h2>{int(df[num_cols[0]].sum())}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi'>📈 ממוצע<br><h2>{round(df[num_cols[0]].mean(),2)}</h2></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='kpi'>⚠️ חריגות<br><h2>{(df[num_cols[0]] > df[num_cols[0]].mean()).sum()}</h2></div>", unsafe_allow_html=True)

# ✅ LAYOUT
left, right = st.columns([2,1])

# ✅ TABLE
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📋 נתונים")
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ✅ CHART
with right:
    if len(num_cols) > 0:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📊 גרף")
        fig = px.bar(df, y=num_cols[0])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ✅ AI SECTION
st.markdown("## 🤖 AI Insights")

if st.button("🚀 הפעל ניתוח"):

    text = df.to_string(index=False)

    with st.spinner("🧠 מנתח נתונים..."):
        res1 = model.generate_content(f"נתח את הנתונים:\n{text}")
        analysis = res1.text

    with st.spinner("🛠️ מייצר המלצות..."):
        res2 = model.generate_content(f"תן תוכנית פעולה:\n{analysis}")
        strategy = res2.text

    colA, colB = st.columns(2)

    with colA:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📋 ניתוח")
        st.markdown(analysis)
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🚀 המלצות")
        st.markdown(strategy)
        st.markdown("</div>", unsafe_allow_html=True)
