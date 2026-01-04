import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="מחשבון תמהיל", layout="wide")

# שימוש בקישור הבסיסי ביותר ללא תוספות
url = "https://docs.google.com/spreadsheets/d/1GHCQVkhzxYL69tiOESk94xHZZkvjWPVTH_Gbg3xWqJE/edit"

st.title("💰 מחשבון תמהיל השקעות")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # ננסה לקרוא את הגיליון הראשון (אינדקס 0) כדי להימנע מבעיות עברית בשם הטאב
    df = conn.read(spreadsheet=url, ttl="0") 
    
    st.success("הנתונים נטענו בהצלחה!")
    st.dataframe(df)

except Exception as e:
    st.error("עדיין יש שגיאת חיבור.")
    st.info("נסה לבדוק אם הגיליון מוגדר כ-Anyone with the link can EDIT")
    st.write(f"שגיאה טכנית: {e}")
