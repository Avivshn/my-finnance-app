import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="דאשבורד ניהול תיק השקעות", layout="wide", initial_sidebar_state="expanded")

# עיצוב CSS מודרני
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div[data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# אתחול נתונים (על בסיס המסמך שלך)
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
    st.session_state.exposure = 72  # אחוז חשיפה רצוי
    st.session_state.monthly_deposit = 4000
    st.session_state.annual_cap = 20520

# תפריט צדדי לעריכת נתונים
with st.sidebar:
    st.header("⚙️ הגדרות ועריכה")
    st.subheader("יתרות נוכחיות")
    for key in st.session_state.data.keys():
        st.session_state.data[key] = st.number_input(f"{key}", value=int(st.session_state.data[key]), step=1000)
    
    st.divider()
    st.subheader("פרמטרים נוספים")
    st.session_state.exposure = st.slider("יעד חשיפה מנייתית (%)", 0, 100, st.session_state.exposure)
    st.session_state.monthly_deposit = st.number_input("הפקדה חודשית למסחר", value=st.session_state.monthly_deposit)

# חישובים
total_assets = sum(st.session_state.data.values())
# הנחה: פנסיה, השתלמות ומסחר הם מנייתיים (לפי הקובץ שלך )
equity_sum = st.session_state.data["פנסיה"] + st.session_state.data["קרן השתלמות - שכיר"] + \
             st.session_state.data["קרן השתלמות - עצמאי"] + st.session_state.data["חשבון מסחר"]
current_exposure_pct = (equity_sum / total_assets) * 100 if total_assets > 0 else 0

# כותרת ראשית
st.title("📊 ניהול תיק השקעות חכם")
st.markdown(f"עדכון אחרון: **{pd.Timestamp.now().strftime('%d/%m/%Y')}**")

# שורת מדדים (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("סה\"כ נכסים", f"₪{total_assets:,.0f}")
col2.metric("חשיפה מנייתית", f"{current_exposure_pct:.1f}%", f"{current_exposure_pct - st.session_state.exposure:.1f}% מיעד")
col3.metric("הפקדה שנתית להשתלמות", f"₪{st.session_state.annual_cap:,.0f}")
col4.metric("יתרה בעו\"ש", f"₪{st.session_state.data['עובר ושב']:,.0f}")

st.divider()

# גרפים
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("חלוקת נכסים")
    fig_pie = go.Figure(data=[go.Pie(labels=list(st.session_state.data.keys()), 
                                   values=list(st.session_state.data.values()), 
                                   hole=.4,
                                   marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']))])
    fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.subheader("ניצול תקרת הפקדה (השתלמות עצמאי)")
    # הנחה שהופקד כבר חלק מהסכום (למשל 900 ש"ח לחודש כפול מספר חודשים)
    deposited_so_far = 900 * pd.Timestamp.now().month 
    remaining_cap = max(0, st.session_state.annual_cap - deposited_so_far)
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = deposited_so_far,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ניצול תקרה (₪)"},
        gauge = {
            'axis': {'range': [None, st.session_state.annual_cap]},
            'bar': {'color': "#1e293b"},
            'steps': [
                {'range': [0, st.session_state.annual_cap*0.8], 'color': "lightgray"},
                {'range': [st.session_state.annual_cap*0.8, st.session_state.annual_cap], 'color': "gray"}]
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# המלצות לשיפור התיק
st.subheader("💡 הצעות לשיפור התיק")
recs = []

if current_exposure_pct > st.session_state.exposure + 5:
    recs.append("⚠️ **חשיפת יתר למניות:** התיק כרגע אגרסיבי מהיעד. שקול להפנות את ההפקדה החודשית הבאה לקרן כספית.")
elif current_exposure_pct < st.session_state.exposure - 5:
    recs.append("📉 **חשיפה נמוכה למניות:** התיק סולידי מדי. מומלץ להגדיל חשיפה ל-S&P 500 או ACWI בתיק המסחר.")

if remaining_cap > 0:
    recs.append(f"💰 **הטבת מס:** נותרו לך ₪{remaining_cap:,.0f} לניצול תקרת השתלמות עצמאי השנה. כדאי להפקיד לפני סוף השנה.")

if st.session_state.data["עובר ושב"] > 20000:
    recs.append("🏦 **עודף מזומן:** יש לך מעל 20,000 ש\"ח בעו\"ש. כדאי להעביר חלק לקרן כספית כדי לקבל ריבית.")

for r in recs:
    st.info(r)

# טבלת נתונים גולמיים
with st.expander("לצפייה בנתונים הגולמיים"):
    df = pd.DataFrame(list(st.session_state.data.items()), columns=['אפיק', 'יתרה (₪)'])
    st.table(df)
