import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. הגדרת כותרת הדף (תמיכה בעברית)
st.set_page_config(page_title="מחשבון השקעות", layout="wide")

# 2. הקישור הנקי (בלי כל מה שבא אחרי ה- /edit)
# שים לב: השארתי רק את החלק המזהה של הקובץ
url = "https://docs.google.com/spreadsheets/d/1GHCQVkhzxYL69tiOESk94xHZZkvjWPVTH_Gbg3xWqJE/edit"

try:
    # יצירת החיבור
    conn = st.connection("gsheets", type=GSheetsConnection)

    # 3. קריאת הנתונים - כאן אנחנו אומרים לו במפורש לחפש את הגיליון בעברית
    # הוספתי worksheet="מחשבון תמהיל"
    df = conn.read(
        spreadsheet=url,
        worksheet="מחשבון תמהיל",
        ttl="10m" # רענון נתונים כל 10 דקות
    )

    st.success("התחברנו בהצלחה!")
    st.write("הנה הנתונים שלך:")
    st.dataframe(df)

except Exception as e:
    st.error("אופס! יש עדיין בעיית חיבור.")
    st.info("ודא שהגדרת את הגיליון כ-'Anyone with the link can EDIT' בגוגל שיטס.")
    st.write(f"פרטי השגיאה: {e}")
