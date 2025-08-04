import streamlit as st

# --- Hardcoded credentials ---
USERNAME = "admin"
PASSWORD = "bank123"

# --- Check login status ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login logic ---
if not st.session_state.logged_in:
    st.title("Login Required")

    with st.form("login_form"):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if user == USERNAME and pwd == PASSWORD:
                st.session_state.logged_in = True
                st.success("Login successful. Reloading...")
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password")
    st.stop()  #  VERY IMPORTANT: Stop rest of the app if not logged in

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc

# Connect to SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=HARIOM\\SQLEXPRESS;DATABASE=NewBankingProject;Trusted_Connection=yes'
)

# Load data
df = pd.read_sql("SELECT * FROM Customers", conn)

# Format phone numbers (optional)
df['Phone'] = df['Phone'].apply(lambda x: f"{str(x)[:5]}-{str(x)[5:]}")

# Streamlit UI
st.set_page_config(page_title="Customer Dashboard", layout="wide")
st.title("📊 Customer Insights Dashboard")

# Search bar
search = st.text_input("🔍 Search by Name or Email")
if search:
    df = df[df['Name'].str.contains(search, case=False) | df['Email'].str.contains(search, case=False)]

# Show data
st.subheader("📋 Customer Table")
st.dataframe(df, use_container_width=True)

# Visualization
st.subheader("📈 Total Customers")
st.metric(label="Count", value=len(df))

# Optional: Pie chart of email domains
df['Domain'] = df['Email'].apply(lambda x: x.split('@')[-1])
domain_counts = df['Domain'].value_counts()
st.subheader("📧 Email Domain Distribution")
st.bar_chart(domain_counts)



#st.write(" Available columns:", df.columns.tolist())



