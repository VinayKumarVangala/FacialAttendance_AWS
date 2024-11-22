import pandas as pd
import streamlit as st
from datetime import datetime

# File paths
date = datetime.now().strftime('%d-%m-%Y')
csv_file_path = f"Attendance/Attendance_{date}.csv"  

def display_attendance():
    try:
        df = pd.read_csv(csv_file_path, on_bad_lines='skip')  # Skip malformed rows
        if df.empty:
            st.write("No attendance data available yet.")
        else:
            st.dataframe(df)
    except pd.errors.ParserError as e:
        st.error(f"Error reading the CSV file: {str(e)}")
    except FileNotFoundError:
        st.error("Attendance file not found. Make sure attendance has been marked.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Streamlit app
st.title("Facial Attendance for the day")
display_attendance()

#streamlit run app.py