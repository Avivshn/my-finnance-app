import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="Portfolio Tracker Pro", layout="wide")

# הזרקת CSS עבור פונט Assistant ועיצוב Dark Mode
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* עיצוב רקע כהה כללי */
    .main {
        background-color: #0e1117;
        color: #e6edf3;
    }

    /* עיצוב כרטיסי המדדים (Metrics) */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* התאמת צבע טקסט במדדים */
    div[data-testid="stMetricValue"] {
        color: #58a6ff !important;
    }

    /* כותרות */
    h1, h2, h3 {
        color: #ffffff;
    }

    /* סיידבר */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-left: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# אתחול State לניהול הפקדות חודשיות
if 'monthly_deposits' not in st.session_state:
    st.session_state.monthly_deposits = {month: 0.0 for month in [
        "ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", 
        "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"
    ]}

if 'data' not in st.session_state:
    st.session_state.data = {
        "פנסיה": 54778,
        "קרן השתלמות - שכיר": 86859,
        "קרן השתלמות - עצמאי": 66007,
        "חשבון מסחר": 115000,
        "קרן ביטחון": 41180,
        "קרן כספית/אג\"ח": 7754,
        "עובר ושב": 11263
    }

# תפריט צד
with st.sidebar:
    st.title("🛠️ ניהול נתונים")
    
    tab1, tab2 = st.tabs(["יתרות", "הפקדות השתלמות"])
    
    with tab1:
        st.subheader("עדכון יתרות")
        for key in st.session_state.data.keys():
            st.session_state.data[key] = st.number_input(f"{key}", value=int(st.session_state.data[key]), step=500)
    
    with tab2:
        st.subheader("פירוט הפקדות 2026")
        for month in st.session_state.monthly_deposits.keys():
            st.session_state.monthly_deposits[month] = st.number_input(f"הפקדה ב{month}", value=float(st.session_state.monthly_deposits[month]), step=100.0)

# חישובים
total_deposited_hst = sum(st.session_state.monthly_deposits.values())
annual_cap = 20520
remaining_cap = max(0, annual_cap - total_deposited_hst)

total_assets = sum(st.session_state.data.values())
equity_sum = st.session_state.data["פנסיה"] + st.session_state.data["קרן השתלמות - שכיר"] + \
             st.session_state.data["קרן השתלמות - עצמאי"] + st.session_state.data["חשבון מסחר"]
exposure_pct = (equity_sum / total_assets) * 100 if total_assets > 0 else 0

# תצוגה ראשית
st.title("🌙 דאשבורד השקעות אישי")
st.markdown("---")

# שורת מדדים
m1, m2, m3, m4 = st.columns(4)
m1.metric("סה\"כ הון מוערך", f"₪{total_assets:,.0f}")
m2.metric("חשיפה מנייתית", f"{exposure_pct:.1f}%")
m3.metric("הופקד להשתלמות", f"₪{total_deposited_hst:,.0f}")
m4.metric("נותר לתקרה", f"₪{remaining_cap:,.0f}")

st.write("") # רווח

# גרפים
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("חלוקת נכסים")
    fig_pie = go.Figure(data=[go.Pie(
        labels=list(st.session_state.data.keys()), 
        values=list(st.session_state.data.values()), 
        hole=.5,
        textinfo='percent',
        marker=dict(colors=['#58a6ff', '#1f6feb', '#238636', '#da3633', '#8957e5', '#d29922', '#30363d'])
    )])
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white", family="Assistant"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("ניצול תקרת הפקדה (עצמאי)")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_deposited_hst,
        number = {'prefix': "₪", 'font': {'color': "#58a6ff", 'family': "Assistant"}},
        gauge = {
            'axis': {'range': [None, annual_cap], 'tickcolor': "white"},
            'bar': {'color': "#58a6ff"},
            'bgcolor': "#30363d",
            'steps': [
                {'range': [0, annual_cap*0.9], 'color': "#161b22"},
                {'range': [annual_cap*0.9, annual_cap], 'color': "#238636"}]
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white", family="Assistant"),
        height=350
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# המלצות
st.markdown("### 💡 תובנות לניהול התיק")
with st.container():
    st.markdown(f"""
    <div style="background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d;">
        • <b>ניצול הטבות מס:</b> נותרו לך ₪{remaining_cap:,.0f} להפקיד לקרן השתלמות כדי למקסם את הטבת המס השנתית.<br>
        • <b>איזון תיק:</b> החשיפה הנוכחית שלך היא {exposure_pct:.1f}%. אם היעד הוא 72%, עליך לבחון הגדלה/הקטנה של רכיבי המניות.<br>
        • <b>נזילות:</b> יש לך ₪{st.session_state.data['עובר ושב']:,.0f} בעובר ושב. ודא שזה תואם את צרכי המחיה המיידיים שלך.
    </div>
    """, unsafe_allow_html=True)
