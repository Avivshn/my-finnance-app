import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="דאשבורד השקעות אישי", layout="wide")

# CSS מקיף לתיקון פונט, צבעים ומרכוז
st.markdown("""
    <style>
    /* טעינת פונט Assistant מ-Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&display=swap');

    /* הגדרות גלובליות */
    * {
        font-family: 'Assistant', sans-serif !important;
        direction: rtl;
    }

    /* רקע כהה לאפליקציה */
    .stApp {
        background-color: #0e1117 !important;
    }

    /* מרכוז כל הטקסטים בדף הראשי בלבד (לא בסיידבר) */
    [data-testid="stMainViewContainer"] .stMarkdown, 
    [data-testid="stMainViewContainer"] h1, 
    [data-testid="stMainViewContainer"] h2, 
    [data-testid="stMainViewContainer"] h3,
    [data-testid="stMainViewContainer"] p {
        text-align: center !important;
        color: #ffffff !important;
    }

    /* צבע לבן בוהק לכל הטקסטים בדף הראשי */
    [data-testid="stMainViewContainer"] span, 
    [data-testid="stMainViewContainer"] label {
        color: #ffffff !important;
    }

    /* עיצוב כרטיסי המדדים (Metrics) - מרכוז וצבע */
    div[data-testid="stMetric"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
        display: block !important;
    }

    /* צבע המדד (המספר) */
    div[data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }
    
    /* כותרת המדד */
    div[data-testid="stMetricLabel"] {
        justify-content: center !important;
        font-size: 1.1rem !important;
    }

    /* תיקון הסיידבר - טקסט לימין (לא ממורכז) */
    [data-testid="stSidebar"] * {
        text-align: right !important;
    }

    /* עיצוב תיבת ההמלצות */
    .recommendation-box {
        background-color: #161b22;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-top: 20px;
        color: #ffffff;
        text-align: center;
    }

    /* הסרת רווחים מיותרים למעלה */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# נתונים מהמסמך שלך 
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

# חישובים לפי נתוני המקור 
total_assets = sum(st.session_state.data.values())
# סכימת החלק המנייתי לפי המסמך
equity_sum = st.session_state.data["פנסיה"] + st.session_state.data["קרן השתלמות - שכיר"] + \
             st.session_state.data["קרן השתלמות - עצמאי"] + st.session_state.data["חשבון מסחר"]
current_exposure = (equity_sum / total_assets) * 100 if total_assets > 0 else 0
target_exposure = 72.0 # כפי שמופיע ב-CSV 

total_deposited_hst = sum(st.session_state.monthly_deposits.values())
annual_cap = 20520 # תקרת הפקדה לפי המסמך 
remaining_cap = max(0, annual_cap - total_deposited_hst)

# דף ראשי
st.title("דאשבורד השקעות אישי")
st.markdown(f"עדכון נתונים: **{pd.Timestamp.now().strftime('%d/%m/%Y')}**")

st.markdown("<br>", unsafe_allow_html=True)

# שורת מדדים (KPIs) - כולם ממורכזים דרך ה-CSS
m1, m2, m3, m4 = st.columns(4)
m1.metric("סה\"כ הון מוערך", f"₪{total_assets:,.0f}")
m2.metric("חשיפה מנייתית", f"{current_exposure:.1f}%")
m3.metric("הופקד להשתלמות", f"₪{total_deposited_hst:,.0f}")
m4.metric("נותר להפקיד", f"₪{remaining_cap:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# גרפים
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("פילוח נכסים")
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(st.session_state.data.keys()), 
        values=list(st.session_state.data.values()), 
        hole=.5,
        marker=dict(colors=['#58a6ff', '#1f6feb', '#238636', '#da3633', '#8957e5', '#d29922', '#30363d']),
        textfont=dict(family="Assistant", color="white")
    )])
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white", family="Assistant"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("ניצול תקרת השתלמות (עצמאי)")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_deposited_hst,
        number = {'prefix': "₪", 'font': {'color': "#58a6ff", 'family': "Assistant", 'size': 50}},
        gauge = {
            'axis': {'range': [None, annual_cap], 'tickcolor': "white"},
            'bar': {'color': "#58a6ff"},
            'bgcolor': "#161b22",
            'steps': [{'range': [0, annual_cap], 'color': "#30363d"}]
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white", family="Assistant"),
        height=350,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# המלצות - בתוך Div מעוצב למרכוז
st.markdown(f"""
    <div class="recommendation-box">
        <h3>💡 הצעות לשיפור התיק</h3>
        <p>• <b>ניצול הטבות מס:</b> השנה הפקדת ₪{total_deposited_hst:,.0f}. נותרו לך עוד ₪{remaining_cap:,.0f} לניצול מלא של תקרת העצמאי.</p>
        <p>• <b>איזון תיק:</b> החשיפה הנוכחית ({current_exposure:.1f}%) מעל יעד ה-{target_exposure}% שהגדרת. שקול להפנות הפקדות למסלולים סולידיים.</p>
        <p>• <b>ניהול מזומן:</b> יתרה של ₪{st.session_state.data['עובר ושב']:,.0f} בעו"ש. וודא שיש לך מספיק נזילות להוצאות הקרובות.</p>
    </div>
""", unsafe_allow_html=True)
