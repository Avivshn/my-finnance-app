import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# הגדרות עמוד
st.set_page_config(page_title="דאשבורד השקעות אישי", layout="wide")

# טעינת פונט Assistant בצורה יציבה (Google Fonts)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# CSS
st.markdown("""
<style>
    :root {
        --bg: #0d1117;
        --card: #161b22;
        --border: #30363d;
        --accent: #58a6ff;
        --text: #ffffff;
        --muted: #c9d1d9;
        --font: 'Assistant', sans-serif;
        --sidebar-w: 380px; /* רוחב סיידבר פתוח */
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

    /* ===== Sidebar: רוחב + מראה מודרני + שליטה כהה ===== */
    [data-testid="stSidebar"] {
        width: var(--sidebar-w) !important;
        min-width: var(--sidebar-w) !important;
        border-left: 1px solid var(--border) !important;
    }
    /* לפעמים Streamlit שם wrapper נוסף */
    section[data-testid="stSidebar"] > div {
        width: var(--sidebar-w) !important;
        min-width: var(--sidebar-w) !important;
    }

    /* כפתור פתיחה/סגירה (החץ) – עושים אותו "כפתור" מודרני */
    [data-testid="collapsedControl"] {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 6px 10px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25) !important;
    }
    /* מוסיפים "hamburger" קטן ליד האייקון הקיים (לא מחליף אותו לגמרי, אבל נותן חיווי ברור) */
    [data-testid="collapsedControl"]::before {
        content: "☰";
        color: var(--muted);
        font-size: 14px;
        margin-left: 8px;
    }

    /* Sidebar יישור */
    [data-testid="stSidebar"] * {
        text-align: right !important;
        color: var(--text) !important;
    }

    hr { border-top: 1px solid var(--border) !important; }

    /* ===== Metrics: מרכוז חזק לכל הקוביות ===== */
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
      gap: 6px !important;
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

    /* ===== Radio/Toggle/Slider: מתקנים רקע לבן ===== */
    [data-baseweb="radio"] label{
      background: var(--card) !important;
      border: 1px solid var(--border) !important;
      border-radius: 10px !important;
      padding: 10px 12px !important;
      margin: 6px 0 !important;
    }
    [data-baseweb="radio"] label *{
      color: var(--text) !important;
    }

    /* slider track/handle (Streamlit/BaseWeb) */
    [data-baseweb="slider"] *{
      color: var(--text) !important;
      font-family: var(--font) !important;
    }
    [data-baseweb="slider"] [role="slider"]{
      outline: none !important;
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

# חודשים
MONTHS_HE = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]

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
    st.session_state.monthly_deposits = {m: 0.0 for m in MONTHS_HE}

# יעד חשיפה - ניתן לשינוי (slider)
if 'target_exposure' not in st.session_state:
    st.session_state.target_exposure = 72.0

# מילוי אוטומטי 900₪ ב-15 לכל חודש (לקרן השתלמות עצמאי) - הגדרה
if 'auto_fill_hst' not in st.session_state:
    st.session_state.auto_fill_hst = True

AUTO_DEPOSIT_AMOUNT = 900.0  # 900 ש"ח

def apply_auto_deposits_900():
    """
    ממלא 900₪ חודשים "שהגיעו לתאריך הפקדה".
    חשוב: Streamlit לא רץ ברקע. זה יתעדכן כשפותחים/מרעננים את האפליקציה.
    """
    now = datetime.now()
    current_month_idx = now.month - 1  # 0..11
    day = now.day

    # עד איזה חודש למלא:
    # אם היום >=15: כולל החודש הנוכחי. אחרת: עד חודש קודם.
    last_month_to_fill = current_month_idx if day >= 15 else current_month_idx - 1

    if last_month_to_fill < 0:
        return  # בתחילת ינואר לפני ה-15 אין מה למלא

    for i in range(0, last_month_to_fill + 1):
        m = MONTHS_HE[i]
        # ממלא רק אם המשתמש לא הזין עדיין משהו
        if float(st.session_state.monthly_deposits.get(m, 0.0)) == 0.0:
            st.session_state.monthly_deposits[m] = AUTO_DEPOSIT_AMOUNT

# Sidebar
with st.sidebar:
    st.header("עריכת נתונים")

    # מצב עריכה
    mode = st.radio("בחר פעולה:", ["עדכון יתרות", "הזנת הפקדות השתלמות"])

    # יעד חשיפה - slider נוח
    st.subheader("יעד חשיפה מנייתית")
    st.session_state.target_exposure = st.slider(
        "בחר יעד (%)",
        min_value=0.0, max_value=100.0,
        value=float(st.session_state.target_exposure),
        step=0.5
    )

    st.divider()

    # מילוי אוטומטי 900₪
    st.subheader("אוטומציה להפקדות עצמאי")
    st.session_state.auto_fill_hst = st.checkbox(
        "מלא אוטומטית 900₪ לכל חודש שהגיע ל-15",
        value=bool(st.session_state.auto_fill_hst)
    )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("החל מילוי עכשיו", use_container_width=True):
            apply_auto_deposits_900()
    with col_b:
        if st.button("אפס הפקדות", use_container_width=True):
            st.session_state.monthly_deposits = {m: 0.0 for m in MONTHS_HE}

    st.caption("הערה: האפליקציה לא רצה ברקע, אז המילוי יקרה כשפותחים/מרעננים את הדאשבורד אחרי ה-15 בחודש.")

    st.divider()

    if mode == "עדכון יתרות":
        for key in st.session_state.data.keys():
            st.session_state.data[key] = st.number_input(
                f"{key}",
                value=int(st.session_state.data[key]),
                step=100
            )
    else:
        st.subheader("הפקדות השתלמות (2026)")
        for month in MONTHS_HE:
            st.session_state.monthly_deposits[month] = st.number_input(
                f"הפקדה ב{month}",
                value=float(st.session_state.monthly_deposits[month]),
                step=50.0
            )

# הפעלת מילוי אוטומטי (אם מסומן)
if st.session_state.auto_fill_hst:
    apply_auto_deposits_900()

# חישובים
total_assets = sum(st.session_state.data.values())
equity_sum = (
    st.session_state.data["פנסיה"]
    + st.session_state.data["קרן השתלמות - שכיר"]
    + st.session_state.data["קרן השתלמות - עצמאי"]
    + st.session_state.data["חשבון מסחר"]
)
current_exposure = (equity_sum / total_assets) * 100 if total_assets > 0 else 0

total_deposited_hst = sum(st.session_state.monthly_deposits.values())
annual_cap = 20520
remaining_cap = max(0, annual_cap - total_deposited_hst)

# דף ראשי
st.title("דאשבורד השקעות אישי")
st.write(f"תאריך עדכון: {pd.Timestamp.now().strftime('%d/%m/%Y')}")
st.markdown("<br>", unsafe_allow_html=True)

# Metrics (עם פסיקים לאלפים)
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
            font=dict(color="#FFFFFF", family="Assistant", size=14)  # לבן (לא אפור)
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

# המלצות (בלי אייקון מנורה)
st.markdown(f"""
    <div class="recommendation-box">
        <h2 style="color: #58a6ff !important;">הצעות לשיפור התיק</h2>
        <p style="font-size: 1.2rem;">• <b>ניצול הטבות מס:</b> נותרו לך <b>₪{remaining_cap:,.0f}</b> לניצול מלא של תקרת קרן ההשתלמות.</p>
        <p style="font-size: 1.2rem;">• <b>איזון תיק:</b> חשיפת המניות כרגע היא {current_exposure:.1f}%. היעד שלך הוא <b>{st.session_state.target_exposure:.1f}%</b>.</p>
        <p style="font-size: 1.2rem;">• <b>נזילות:</b> יתרת העו"ש עומדת על ₪{st.session_state.data['עובר ושב']:,.0f}.</p>
    </div>
""", unsafe_allow_html=True)
