import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="דאשבורד השקעות אישי", layout="wide")

# טעינת פונט Assistant בצורה יציבה (Google Fonts)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# CSS לתיקון פונט, צבעים, מרכוז מלא, שדות קלט כהים
st.markdown("""
<style>
    :root {
        --bg: #0d1117;
        --card: #161b22;
        --border: #30363d;
        --accent: #58a6ff;
        --text: #ffffff;
        --font: 'Assistant', sans-serif;
    }

    /* פונט + RTL + צבעים */
    html, body, [class*="css"], .stApp, .stMarkdown, p, span, label, div, h1,h2,h3,h4,h5 {
        font-family: var(--font) !important;
        direction: rtl;
        color: var(--text) !important;
    }

    /* רקע כהה אחיד (כולל סיידבר) */
    .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: var(--bg) !important;
    }

    /* מרכז את הקונטיינר הראשי בלי לשבור columns */
    [data-testid="stMainViewContainer"] .block-container {
        max-width: 1200px;
        margin: 0 auto;
        text-align: center !important;
    }

    /* כותרות */
    h1, h2, h3, h4, h5, .stMarkdown div {
        text-align: center !important;
        width: 100%;
        color: var(--text) !important;
    }

    /* ===== Metrics: מרכוז חזק לכל הקוביות ולכל רכיבי הפנים ===== */
    div[data-testid="stMetric"]{
      background-color: var(--card) !important;
      border: 1px solid var(--border) !important;
      border-radius: 12px !important;
      padding: 22px !important;

      display:flex !important;
      flex-direction:column !important;
      align-items:center !important;
      justify-content:center !important;
      text-align:center !important;
      width:100% !important;
    }

    div[data-testid="stMetric"] > div,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricDelta"]{
      width:100% !important;
      display:flex !important;
      justify-content:center !important;
      align-items:center !important;
      text-align:center !important;
    }

    div[data-testid="stMetric"] *{
      text-align:center !important;
      justify-content:center !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricLabel"] *{
      color: var(--text) !important;
      font-size: 1.15rem !important;
      font-weight: 600 !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] *{
      color: var(--accent) !important;
      font-size: 2.35rem !important;
      font-weight: 700 !important;
      line-height: 1.1 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { border-left: 1px solid var(--border) !important; }
    [data-testid="stSidebar"] * { text-align: right !important; color: var(--text) !important; }

    hr { border-top: 1px solid var(--border) !important; }

    /* ===== Inputs (number_input וכו’) כהים וקריאים ===== */
    [data-baseweb="input"] > div{
      background-color: var(--card) !important;
      border: 1px solid var(--border) !important;
    }

    [data-baseweb="input"] input{
      color: var(--text) !important;
      background-color: transparent !important;
      font-family: var(--font) !important;
      text-align: right !important;
    }

    .stNumberInput label, .stTextInput label, .stSelectbox label {
      color: var(--text) !important;
    }

    /* טקסטים קטנים של Streamlit שלפעמים יוצאים אפורים */
    .stCaption, small, [data-testid="stCaptionContainer"] {
      color: var(--text) !important;
      opacity: 1 !important;
    }

    /* עיצוב תיבת ההמלצות */
    .recommendation-box {
        background-color: var(--card);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid var(--accent);
        margin-top: 30px;
        text-align: center;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# נתונים גולמיים
if 'data' not in st.session_state:
    st.session_state.data = {
        "פנסיה": 54778,
        "קרן השתלמות - שכיר": 86859,
        "קרן השתלמות - עצמאי": 66007,
        "חשבון מסחר": 115000,
        "קרן ביטחון": 41180,
        "קרן כספית / אג\"ח": 7754,
        "עובר ושב": 11263
    }

if 'monthly_deposits' not in st.session_state:
    st.session_state.monthly_deposits = {m: 0.0 for m in [
        "ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני",
        "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"
    ]}

# Sidebar
with st.sidebar:
    st.header("עריכת נתונים")
    mode = st.radio("בחר פעולה:", ["עדכון יתרות", "הזנת הפקדות השתלמות"])

    if mode == "עדכון יתרות":
        for key in st.session_state.data.keys():
            st.session_state.data[key] = st.number_input(f"{key}", value=int(st.session_state.data[key]))
    else:
        st.subheader("הפקדות השתלמות (2026)")
        for month in st.session_state.monthly_deposits.keys():
            st.session_state.monthly_deposits[month] = st.number_input(
                f"הפקדה ב{month}",
                value=float(st.session_state.monthly_deposits[month])
            )

# חישובים
total_assets = sum(st.session_state.data.values())
equity_sum = (
    st.session_state.data["פנסיה"]
    + st.session_state.data["קרן השתלמות - שכיר"]
    + st.session_state.data["קרן השתלמות - עצמאי"]
    + st.session_state.data["חשבון מסחר"]
)
current_exposure = (equity_sum / total_assets) * 100 if total_assets > 0 else 0
target_exposure = 72.0

total_deposited_hst = sum(st.session_state.monthly_deposits.values())
annual_cap = 20520
remaining_cap = max(0, annual_cap - total_deposited_hst)

# דף ראשי
st.title("דאשבורד השקעות אישי")
st.write(f"תאריך עדכון: {pd.Timestamp.now().strftime('%d/%m/%Y')}")
st.markdown("<br>", unsafe_allow_html=True)

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric('סה"כ הון מוערך', f"₪{total_assets:,.0f}")
m2.metric("חשיפה מנייתית", f"{current_exposure:.1f}%")
m3.metric("הופקד להשתלמות", f"₪{total_deposited_hst:,.0f}")
m4.metric("נותר להפקיד", f"₪{remaining_cap:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("פילוח נכסים")
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(st.session_state.data.keys()),
        values=list(st.session_state.data.values()),
        hole=.5,
        marker=dict(colors=['#58a6ff', '#1f6feb', '#238636', '#da3633', '#8957e5', '#d29922', '#40444b']),
        textfont=dict(family="Assistant", color="white", size=14)
    )])
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FFFFFF", family="Assistant"),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.3,
            xanchor="center", x=0.5,
            font=dict(color="#FFFFFF", family="Assistant", size=14)
        ),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("ניצול תקרת השתלמות")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_deposited_hst,
        number={'prefix': "₪", 'font': {'color': "#58a6ff", 'family': "Assistant", 'size': 60}},
        gauge={
            'axis': {
                'range': [None, annual_cap],
                'tickcolor': "white",
                'tickfont': {'color': "white", 'family': "Assistant", 'size': 14}
            },
            'bar': {'color': "#58a6ff"},
            'bgcolor': "#161b22",
            'steps': [{'range': [0, annual_cap], 'color': "#30363d"}]
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#FFFFFF", family="Assistant"),
        height=350,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# המלצות
st.markdown(f"""
    <div class="recommendation-box">
        <h2 style="color: #58a6ff !important;">💡 הצעות לשיפור התיק</h2>
        <p style="font-size: 1.2rem;">• <b>ניצול הטבות מס:</b> נותרו לך <b>₪{remaining_cap:,.0f}</b> לניצול מלא של תקרת קרן ההשתלמות.</p>
        <p style="font-size: 1.2rem;">• <b>איזון תיק:</b> חשיפת המניות כרגע היא {current_exposure:.1f}%. היעד שלך הוא <b>{target_exposure}%</b>.</p>
        <p style="font-size: 1.2rem;">• <b>נזילות:</b> יתרת העו"ש עומדת על ₪{st.session_state.data['עובר ושב']:,.0f}.</p>
    </div>
""", unsafe_allow_html=True)
