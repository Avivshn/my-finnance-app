import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="דאשבורד השקעות אישי", layout="wide")

# CSS "אלים" לתיקון פונט, צבעים ומרכוז מלא
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&display=swap');

    /* הגדרת פונט וצבע טקסט גלובלי - לבן ותכלת בלבד */
    html, body, [class*="css"], .stApp, .stMarkdown, p, span, label {
        font-family: 'Assistant', sans-serif !important;
        direction: rtl;
        color: #FFFFFF !important; /* לבן בוהק לכל הטקסט */
    }

    /* רקע כהה אחיד לכל האפליקציה (כולל סיידבר) */
    .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: #0d1117 !important;
    }

    /* מרכוז אגרסיבי של כל התוכן בדף הראשי */
    [data-testid="stMainViewContainer"] .block-container {
        max-width: 1200px;
        margin: 0 auto;
        text-align: center !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* מרכוז כותרות וטקסטים */
    h1, h2, h3, h4, h5, .stMarkdown div {
        text-align: center !important;
        width: 100%;
        color: #FFFFFF !important;
    }

    /* עיצוב כרטיסי המדדים (Metrics) */
    div[data-testid="stMetric"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 25px !important;
        text-align: center !important;
    }

    /* צבע המדד (המספר) - תכלת */
    div[data-testid="stMetricValue"] > div {
        color: #58a6ff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        justify-content: center !important;
    }
    
    /* כותרת המדד - לבן */
    div[data-testid="stMetricLabel"] > div {
        color: #FFFFFF !important;
        justify-content: center !important;
        font-size: 1.2rem !important;
    }

    /* סיידבר - יישור לימין וצבע לבן */
    [data-testid="stSidebar"] {
        border-left: 1px solid #30363d !important;
    }
    [data-testid="stSidebar"] * {
        text-align: right !important;
        color: #FFFFFF !important;
    }

    /* הסרת קווים אפורים מיותרים */
    hr { border-top: 1px solid #30363d !important; }

    /* עיצוב תיבת ההמלצות */
    .recommendation-box {
        background-color: #161b22;
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #58a6ff;
        margin-top: 30px;
        text-align: center;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# נתונים גולמיים מהמסמך שלך 
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
    st.session_state.monthly_deposits = {m: 0.0 for m in ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]}

# תפריט צד (Sidebar)
with st.sidebar:
    st.header("עריכת נתונים")
    mode = st.radio("בחר פעולה:", ["עדכון יתרות", "הזנת הפקדות השתלמות"])
    
    if mode == "עדכון יתרות":
        for key in st.session_state.data.keys():
            st.session_state.data[key] = st.number_input(f"{key}", value=int(st.session_state.data[key]))
    else:
        st.subheader("הפקדות השתלמות (2026)")
        for month in st.session_state.monthly_deposits.keys():
            st.session_state.monthly_deposits[month] = st.number_input(f"הפקדה ב{month}", value=float(st.session_state.monthly_deposits[month]))

# חישובים מבוססי מקור 
total_assets = sum(st.session_state.data.values()) # סה"כ צבירה: 382,841 ש"ח
equity_sum = st.session_state.data["פנסיה"] + st.session_state.data["קרן השתלמות - שכיר"] + \
             st.session_state.data["קרן השתלמות - עצמאי"] + st.session_state.data["חשבון מסחר"]
current_exposure = (equity_sum / total_assets) * 100 if total_assets > 0 else 0
target_exposure = 72.0 # יעד חשיפה מבוסס מקור 

total_deposited_hst = sum(st.session_state.monthly_deposits.values())
annual_cap = 20520 # תקרת הפקדה שנתית 
remaining_cap = max(0, annual_cap - total_deposited_hst)

# דף ראשי - הכל במרכז
st.title("דאשבורד השקעות אישי")
st.write(f"תאריך עדכון: {pd.Timestamp.now().strftime('%d/%m/%Y')}")

st.markdown("<br>", unsafe_allow_html=True)

# שורת מדדים - כולם ממורכזים בלבן ותכלת
m1, m2, m3, m4 = st.columns(4)
m1.metric("סה\"כ הון מוערך", f"₪{total_assets:,.0f}")
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
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("ניצול תקרת השתלמות")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_deposited_hst,
        number = {'prefix': "₪", 'font': {'color': "#58a6ff", 'family': "Assistant", 'size': 60}},
        gauge = {
            'axis': {'range': [None, annual_cap], 'tickcolor': "white"},
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

# המלצות - בתוך Div מעוצב עם מסגרת תכלת
st.markdown(f"""
    <div class="recommendation-box">
        <h2 style="color: #58a6ff !important;">💡 הצעות לשיפור התיק</h2>
        <p style="font-size: 1.2rem;">• <b>ניצול הטבות מס:</b> נותרו לך <b>₪{remaining_cap:,.0f}</b> לניצול מלא של תקרת קרן ההשתלמות.</p>
        <p style="font-size: 1.2rem;">• <b>איזון תיק:</b> חשיפת המניות כרגע היא {current_exposure:.1f}%. היעד שלך הוא <b>{target_exposure}%</b>.</p>
        <p style="font-size: 1.2rem;">• <b>נזילות:</b> יתרת העו"ש עומדת על ₪{st.session_state.data['עובר ושב']:,.0f}.</p>
    </div>
""", unsafe_allow_html=True)
