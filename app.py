import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

st.set_page_config(layout="wide")

# 🎨 Bootstrap‑Like Design
st.markdown("""
<style>
body {
    direction: RTL;
    background: #0f172a;
}

.main-card {
    background: #1e293b;
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.kpi {
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 18px;
}

button[kind="primary"] {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}

.sidebar .sidebar-content {
    background: #020617;
}
</style>
""", unsafe_allow_html=True)

# 🔐 API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ חסר API")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# 🧭 Sidebar
st.sidebar.title("⚙️ Control Panel")
uploaded_file = st.sidebar.file_uploader("📁 העלאת קובץ", type=["xlsx", "csv"])

# כותרת
st.markdown("<h1 style='text-align:center;'>📊 License Intelligence</h1>", unsafe_allow_html=True)

if not uploaded_file:
    st.info("⬅️ העלה קובץ")
    st.stop()

# קריאת דאטה
if uploaded_file.name.endswith("xlsx"):
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_csv(uploaded_file)

# ✅ KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='kpi'>📦 רשומות<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

num_cols = df.select_dtypes(include="number").columns

if len(num_cols) > 0:
    with col2:
        st.markdown(f"<div class='kpi'>💰 סה\"כ<br><h2>{int(df[num_cols[0]].sum())}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='kpi'>📈 ממוצע<br><h2>{round(df[num_cols[0]].mean(),2)}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# ✅ גרף
if len(num_cols) > 0:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    fig = px.bar(df, y=num_cols[0], title="ניתוח נתונים")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ✅ טבלה
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ✅ AI
if st.button("🚀 ניתוח חכם"):

    text = df.to_string(index=False)

    with st.spinner("🧠 מנתח..."):
        res1 = model.generate_content(f"נתח את הנתונים:\n{text}")
        report1 = res1.text

    with st.spinner("🛠️ מייצר אסטרטגיה..."):
        res2 = model.generate_content(f"תן המלצות:\n{report1}")
        report2 = res2.text

    colA, colB = st.columns(2)

    with colA:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 ניתוח")
        st.markdown(report1)
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("### 🚀 המלצות")
        st.markdown(report2)
        st.markdown("</div>", unsafe_allow_html=True)
