import streamlit as st
import plotly.graph_objs as go 
import plotly.express as px
import pandas as pd

def get_dataframe():

    # Publish csv link of google sheet from where the data is pulled
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTpN8azJXj7YSyfBkK9Kkal4tKrlqaL7AuOslSwH2H_wa6VNnumhlWFxoc-om97-s9W1-_xD6qsEuWt/pub?output=csv"
    # Reading csv file
    df = pd.read_csv(url)
    return df

# Making a variable for dataframe function
df = get_dataframe()

# Setting page to wide orientation
st.set_page_config(layout="wide")

# Dashboard Title
st.markdown("<h1 style='text-align:center; color: maroon;font-size:60px;'>Consumer Financial Protection Bureau Complaints Dashboard</h1>", unsafe_allow_html=True)

# Selecting state column and remove duplicates, then sorting A-Z and inserting Str Select State which shows all the data if selected
dim_state = list(df['state'].drop_duplicates())
dim_state.sort(reverse=False)
dim_state.insert(0,'Select State')

# This will make the filter dropdown and KPI metrics
col1, col2, col3, col4, col5 = st.columns([3,1.75,1.75,1.75,1.75])
filter = col1.selectbox('States', dim_state)
if filter =="Select State":
    pass
else:
    df = df[df['state']==(filter)]

total_complaints = df['count'].sum()
closed_complaints = df.loc[df['company_response'].str.contains(pat='Closed'), 'count'].sum()
timely_complaints = df.loc[df['timely'] == 'Yes', 'count'].sum()
timely_complaints_ratio = timely_complaints/total_complaints
in_progess_complaints = df.loc[df['company_response'] == 'In progress', 'count'].sum()

dim_state = df['state']
col2.metric("Total Complaints", "{:,}".format(total_complaints))
col3.metric("Closed Complaints","{:,}".format(closed_complaints))
col4.metric("Timely Complaints %%", "{:.1%}".format(timely_complaints_ratio))
col5.metric("In Progress Complaints","{:,}".format(in_progess_complaints))

labels = df.groupby('product')['count'].sum().reset_index().sort_values(by='count')['product'].values
values = df.groupby('product')['count'].sum().reset_index().sort_values(by='count')['count'].values

labels_month = df.groupby('month_year')['count'].sum().reset_index().sort_values(by='month_year')['month_year'].values
values_month = df.groupby('month_year')['count'].sum().reset_index().sort_values(by='month_year')['count'].values
df2 = df.groupby('product').sum()

labels_channel = df.groupby('submitted_via')['count'].sum().reset_index().sort_values(by='submitted_via')['submitted_via'].values
values_channel = df.groupby('submitted_via')['count'].sum().reset_index().sort_values(by='submitted_via')['count'].values

issue = df.groupby(['issue','sub_issue'])['count'].sum().reset_index().sort_values(by='issue')['issue'].values
sub_issue = df.groupby(['issue','sub_issue'])['count'].sum().reset_index().sort_values(by='issue')['sub_issue'].values

# Create a container with 2 Columns dividing equally
with st.container():
    col1, col2 = st.columns(2)
    
    # Creates a Horizontal Bar Chart
    fig = px.bar(df, x=values, y=labels, orientation='h',title='Number of Complaints by Products',color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',autosize=True)
    col1.write(fig)

    # Creates a Line Chart
    data = pd.DataFrame(values_month,labels_month)
    fig = px.line(df, x=labels_month, y=values_month, title='Number of Complaints by Month & Year',color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',autosize=True)
    col2.write(fig)

# Create a container with 2 Columns dividing equally
with st.container():
    col1, col2 = st.columns(2)

    # Creates a Pie Chart
    fig = px.pie(df, values=values_channel, names=labels_channel, title='Breakup by Channels',hole=0.3,color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',autosize=True)
    col1.write(fig)

    # Create a Treemap
    tf = df.groupby(['issue','sub_issue'],as_index=True).size().reset_index(name='count')
    fig = px.treemap(tf, path=[px.Constant("Treemap"), 'issue','sub_issue'],values='count',title='Treemap by Issue and Sub Issue',color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=25, l=25, r=25, b=25))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',autosize=True)
    col2.write(fig)