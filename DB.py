# import library
import pandas as pd #data manipulate
import streamlit as st #web abb (Dashboard (DB))
import numpy as np # function (math,arrays)
import matplotlib.pyplot as plt # visualized
import seaborn as sns # visualized
import plotly.express as px # ***visualized


#layout
st.set_page_config(
    page_title="Dashboard",
    layout = 'wide',
)
# Add custom CSS to center-align the title
st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Center-aligned title
st.markdown("<h1 class='title'>Dashboard For Board of Directors</h1>", unsafe_allow_html=True)

# Define file paths
title_csv_path = 'title.csv'
worker_csv_path = 'worker.csv'
bonus_csv_path = 'bonus.csv'

# Function for data preprocessing
def preprocess_data(worker_df, title_df, bonus_df):
    # Merge worker and title data
    merged_df = worker_df.merge(title_df, left_on='WORKER_ID', right_on='WORKER_REF_ID', how='left')

    # Sum bonus amounts per worker
    bonus_data = bonus_df.groupby('WORKER_REF_ID')['BONUS_AMOUNT'].sum().reset_index()

    # Merge bonus data with worker data
    merged_df = merged_df.merge(bonus_data, left_on='WORKER_ID', right_on='WORKER_REF_ID', how='left')

    # Fill missing values in TITLE and BONUS columns
    merged_df['TITLE'] = merged_df['WORKER_TITLE'].fillna('Executive')
    merged_df['BONUS_AMOUNT'] = merged_df['BONUS_AMOUNT'].fillna(0)

    # Calculate Full Name
    merged_df['Full Name'] = merged_df['FIRST_NAME'] + ' ' + merged_df['LAST_NAME']

    # Convert JOINING_DATE to datetime
    merged_df['JOINING_DATE'] = pd.to_datetime(merged_df['JOINING_DATE'])
    

    return merged_df

# Load data
title_data = pd.read_csv(title_csv_path)
worker_data = pd.read_csv(worker_csv_path)
bonus_data = pd.read_csv(bonus_csv_path)

# Preprocess data
processed_data = preprocess_data(worker_data, title_data, bonus_data)

# Calculate Monthly Salary
processed_data['SALARY'] = round(processed_data['SALARY'] / 12, 2)
processed_data['YSALARY'] = round(processed_data['SALARY'] * 12, 2)

col0, col1, col2, col3 = st.columns(4)

col0.metric('**Total Salary (Yearly)**',f'{round((processed_data["SALARY"].sum())*12,2)}')
col1.metric('**Total Salary (Monthly)**',f'{round((processed_data["SALARY"].sum()),2)}')
col2.metric("**Average Salary (Yearly)**", f'{round((processed_data["SALARY"].mean())*12,2)}')
col3.metric("**Average Salary (Monthly)**", f'{round((processed_data["SALARY"].mean()),2)}')

# Create a bar plot using Plotly Express
fig000= px.bar(processed_data.sort_values(by='YSALARY', ascending=False).drop_duplicates(['Full Name']), y='YSALARY', x='Full Name', title='Employee Salary (Yearly)', color='Full Name',
             text='YSALARY')

# Create a bar plot using Plotly Express
fig00= px.bar(processed_data.sort_values(by='SALARY', ascending=False).drop_duplicates(['Full Name']), y='SALARY', x='Full Name', title='Employee Salary (Monthly)', color='Full Name',
             text='SALARY')

ys, ms = st.tabs(['Employee Salary (Yearly)', 'Employee Salary (Monthly)'])
with ys:
    st.plotly_chart(fig000, use_container_width=True)
with ms:
    st.plotly_chart(fig00, use_container_width=True)

# Group data by 'DEPARTMENT' and count the number of employees in each department
department_counts = processed_data.groupby('DEPARTMENT').size().reset_index(name='COUNT').sort_values(by='COUNT')

# Create a bar plot using Plotly Express
fig0= px.bar(department_counts, y='DEPARTMENT', x='COUNT', title='Employee Count by Department', color='DEPARTMENT',
             text='COUNT')

# Group data by 'DEPARTMENT' and count the number of employees in each department
title_counts = processed_data.groupby('TITLE').size().reset_index(name='COUNT').sort_values(by='COUNT')

# Create a bar plot using Plotly Express
fig1 = px.bar(title_counts, y='TITLE', x='COUNT', title='Employee Count by Title', color='TITLE',
              text='COUNT')

# Group data by 'DEPARTMENT' and calculate the sum of salaries in each department
department_sum = processed_data.groupby('DEPARTMENT')['SALARY'].sum().reset_index(name='SUM').sort_values(by='SUM')

# Create a bar plot using Plotly Express
fig2 = px.bar(department_sum, y='DEPARTMENT', x='SUM', title='Employee Sum Salary by Department (Monthly)', color='DEPARTMENT',
              text='SUM')

# Group data by 'TITLE' and calculate the sum of salaries for each title
title_sum = processed_data.groupby('TITLE')['SALARY'].sum().reset_index(name='SUM').sort_values(by='SUM')

# Create a bar plot using Plotly Express
fig3 = px.bar(title_sum, y='TITLE', x='SUM', title='Employee Sum Salary by Title (Monthly)', color='TITLE',
              text='SUM')

col1, col2 = st.columns(2)
with col1:
    department, title = st.tabs(['Employee Count by Department', 'Employee Count by Title'])
    with department:
        st.plotly_chart(fig0, use_container_width=True)
    with title:
        st.plotly_chart(fig1, use_container_width=True)
with col2:
    department, title = st.tabs(['Employee Sum Salary Department (Monthly)', 'Employee Sum Salary by Title (Monthly)'])
    with department:
        st.plotly_chart(fig2, use_container_width=True)
    with title:
        st.plotly_chart(fig3, use_container_width=True)
