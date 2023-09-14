# Core Pkgs
import streamlit as st 
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="SQLPlayground",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DB Mgmt
import sqlite3 
conn = sqlite3.connect('data/admission.sqlite')
c = conn.cursor()

# Fxn Make Execution
def sql_executor(raw_code):
    c.execute(raw_code)
    data = c.fetchall()
    return data 

def get_table_schema(table_name):
    c.execute(f"PRAGMA table_info({table_name})")
    return c.fetchall()

Admission = ['Serial No.','GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research','Admission Chance']

def main():
    st.title("SQLPlayground")
    st.image('lucas2.jpg', width=100)

    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("HomePage")

        # Columns/Layout
        col1,col2 = st.columns(2)

        with col1:
            with st.form(key='query_form'):
                raw_code = st.text_area("SQL Code Here")
                submit_code = st.form_submit_button("Execute")

            # Table of Info
            with st.expander("Table Info"):
                table_info = {'Admission':Admission}
                st.json(table_info)

                # Schema display
                st.subheader("Schema for Admission")
                schema_info = get_table_schema("Admission")
                for column in schema_info:
                    st.write(f"Name: {column[1]}, Type: {column[2]}")
                
        # Results Layouts
        with col2:
            if submit_code:
                st.info("Query Submitted")
                st.code(raw_code)

                # Results 
                query_results = sql_executor(raw_code)
                with st.expander("Results"):
                    st.write(query_results)

                with st.expander("Pretty Table"):
                    query_df = pd.DataFrame(query_results)
                    st.dataframe(query_df)

    else:
        st.subheader("About")
        st.write("""
        Welcome to Lucas'app
        """)

if __name__ == '__main__':
    main()
