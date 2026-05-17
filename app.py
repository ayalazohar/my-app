import streamlit as st
import pandas as pd
import google.generativeai as genai

from streamlit_elements import elements, mui, html

st.set_page_config(layout="wide")

# 🔐 API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing API Key")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx"])

# ✅ START SCREEN (אמיתי)
if not uploaded_file:

    with elements("landing"):
        mui.Box(
            sx={
                "height": "90vh",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "gap": 3,
            },
            children=[
                mui.Typography(
                    "License Intelligence",
                    variant="h2",
                    sx={"fontWeight": "bold"}
                ),
                mui.Typography(
                    "AI-powered license optimization platform",
                    variant="h5",
                    color="text.secondary"
                ),
                mui.Button("Upload file to start", variant="contained")
            ],
        )

    st.stop()

# ✅ DATA
if uploaded_file.name.endswith("xlsx"):
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_csv(uploaded_file)

# ✅ DASHBOARD אמיתי
with elements("dashboard"):

    mui.Grid(
        container=True,
        spacing=2,
        children=[

            # KPI 1
            mui.Grid(
                item=True,
                xs=3,
                children=mui.Paper(
                    sx={"padding": 3},
                    children=[
                        mui.Typography("Records"),
                        mui.Typography(str(len(df)), variant="h4")
                    ]
                )
            ),

            # KPI 2
            mui.Grid(
                item=True,
                xs=3,
                children=mui.Paper(
                    sx={"padding": 3},
                    children=[
                        mui.Typography("Columns"),
                        mui.Typography(str(len(df.columns)), variant="h4")
                    ]
                )
            )
        ]
    )

# ✅ AI
if st.button("Run AI"):

    text = df.to_string(index=False)

    res = model.generate_content(f"Analyze:\n{text}")

    st.write(res.text)
