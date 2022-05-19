import streamlit as st
import plotly.graph_objs as go 
import plotly.express as px
import pandas as pd

def get_dataframe():

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTpN8azJXj7YSyfBkK9Kkal4tKrlqaL7AuOslSwH2H_wa6VNnumhlWFxoc-om97-s9W1-_xD6qsEuWt/pub?output=csv"
    df = pd.read_csv(url)
    return df

df = get_dataframe()

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align:center; color: maroon;font-size:60px;'>Consumer Financial Protection Bureau Complaints Dashboard</h1>", unsafe_allow_html=True)

dim_state = list(df['state'].drop_duplicates())
dim_state.sort(reverse=False)
dim_state.insert(0,'Select State')

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
# pies = pie.columns['submitted_via','count']

issue = df.groupby(['issue','sub_issue'])['count'].sum().reset_index().sort_values(by='issue')['issue'].values
sub_issue = df.groupby(['issue','sub_issue'])['count'].sum().reset_index().sort_values(by='issue')['sub_issue'].values

with st.container():
    col1, col2 = st.columns(2)
    fig = px.bar(df, x=values, y=labels, orientation='h',title='Number of Complaints by Products',color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',autosize=True)
    col1.write(fig)

    data = pd.DataFrame(values_month,labels_month)
    fig = px.line(df, x=labels_month, y=values_month, title='Number of Complaints by Month & Year',color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',autosize=True)
    col2.write(fig)

with st.container():
    col1, col2 = st.columns(2)
    fig = px.pie(df, values=values_channel, names=labels_channel, title='Breakup by Channels',hole=0.3,color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',autosize=True)
    col1.write(fig)

    fig = px.treemap(df, path=[px.Constant("Treemap"), 'issue','sub_issue'],values='count',title='Treemap by Issue and Sub Issue',color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=25, l=25, r=25, b=25))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',autosize=True)
    col2.write(fig)