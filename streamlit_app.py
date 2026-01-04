import streamlit as st
from streamlit_gsheets import GSheetsConnection

# הגדרת חיבור לגוגל שיטס
url = "קישור_האקסל_שלך_כאן"
conn = st.connection("gsheets", type=GSheetsConnection)

# קריאת הנתונים
df = conn.read(spreadsheet=url, usecols=[0, 1]) # קורא עמודות A ו-B למשל

st.write("נתונים מהאקסל:", df)

# עדכון נתונים (דוגמה)
if st.button("עדכן שכר"):
    # כאן נוסיף לוגיקה שכותבת חזרה לתא ספציפי
    st.success("הנתונים נשלחו לאקסל!")
