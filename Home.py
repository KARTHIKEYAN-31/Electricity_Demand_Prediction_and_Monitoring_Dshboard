import pandas as pd
import numpy as np
import streamlit as st 
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error
from datetime import datetime, timedelta
import warnings
import import_data as data
import css
import plotly.express as px
import plotly.graph_objects as go
warnings.filterwarnings('ignore')

css.css()

st.title('US Electricity Production Monitoring Dashboard')

if 'sel_df' not in st.session_state:
    st.session_state['sel_df'] = None
if 'sel_df_1' not in st.session_state:
    st.session_state['sel_df_1'] = None
if 'demand' not in st.session_state:
    st.session_state['demand'] = None

final_df = data.final_df.copy()
demand = data.demand.copy()
date_list = final_df.index

sel_date = st.sidebar.date_input(' ', value = date_list[-1],
                               min_value = date_list[0], max_value = date_list[-1],
                               format="YYYY-MM-DD")




if sel_date == date_list[0].date():

    st.session_state.sel_df = final_df.loc[sel_date:sel_date+timedelta(days=1)]
    st.session_state.sel_df = st.session_state.sel_df.drop(sel_date+timedelta(days=1))

    st.session_state.demand = demand.set_index('date').loc[sel_date:sel_date+timedelta(days=1)]
    st.session_state.demand = st.session_state.demand.drop(sel_date+timedelta(days=1))
    # st.session_state.sel_df = data.final_df.loc[sel_date:sel_date+timedelta(days=1)]
    # st.session_state.sel_df = st.session_state.sel_df.drop(sel_date+timedelta(days=1))
    st.session_state.sel_df_1 = final_df[sel_date:sel_date+timedelta(days=1)].groupby(data.final_df[sel_date:sel_date+timedelta(days=1)].index.date).sum()
    st.session_state.sel_df_1 = st.session_state.sel_df_1.drop(sel_date+timedelta(days=1))

    def get_delta(col):
        return 0

elif sel_date == date_list[-1].date():
    st.session_state.sel_df = final_df.loc[sel_date:]

    st.session_state.sel_df_1 = final_df[sel_date-timedelta(days=1):].groupby(data.final_df[sel_date-timedelta(days=1):].index.date).sum()

    st.session_state.demand = demand.set_index('date').loc[sel_date:]
    def get_delta(col):
        return st.session_state.sel_df_1.iloc[1][col] - st.session_state.sel_df_1.iloc[0][col]

else:

    st.session_state.sel_df = final_df.loc[sel_date:sel_date+timedelta(days=1)]
    st.session_state.sel_df = st.session_state.sel_df.drop(sel_date+timedelta(days=1))

    st.session_state.demand = demand.set_index('date').loc[sel_date:sel_date+timedelta(days=1)]
    st.session_state.demand = st.session_state.demand.drop(sel_date+timedelta(days=1))
    # st.session_state.sel_df = data.final_df.loc[sel_date-timedelta(days=1):sel_date+timedelta(days=1)]
    # st.session_state.sel_df = st.session_state.sel_df.drop(sel_date+timedelta(days=1))
    st.session_state.sel_df_1 = final_df[sel_date-timedelta(days=1):sel_date+timedelta(days=1)].groupby(data.final_df[sel_date-timedelta(days=1):sel_date+timedelta(days=1)].index.date).sum()
    st.session_state.sel_df_1 = st.session_state.sel_df_1.drop(sel_date+timedelta(days=1))

    def get_delta(col):
        return st.session_state.sel_df_1.iloc[1][col] - st.session_state.sel_df_1.iloc[0][col]


st.session_state.sel_df['Total Power Produced'] = st.session_state.sel_df.apply(lambda row: row.sum(), axis=1)
st.session_state.sel_df['Power in Demand'] = st.session_state.demand['megawatthours'].values
st.session_state.sel_df['Power Shortage'] = st.session_state.sel_df['Total Power Produced'] - st.session_state.sel_df['Power in Demand']

css.vertival_space(20)


c1, c2, c3 = st.columns(3)
if st.session_state.sel_df['Total Power Produced'].sum() < st.session_state.sel_df['Power in Demand'].sum():
    colour = 'red'
else: 
    colour = 'green'

with c1:
    fig = go.Figure(go.Indicator (
        mode = "number",
        value = st.session_state.sel_df['Total Power Produced'].sum(),
        title = {"text": "Total Power Produced", "font": {"size": 20}, "align": "left"},
        number = { 'font': {'size': 60}, },
        domain = {'x': [0, 1], 'y': [0, 1]}))

    fig.update_layout(paper_bgcolor = "#262730", height = 200,
                       margin = dict(l=30, r=30, b=0, t=0, pad=0))
    st.plotly_chart(fig, use_container_width=True)
    

with c2:
    fig = go.Figure(go.Indicator (
        mode = "number",
        value = st.session_state.sel_df['Power in Demand'].sum(),
        title = {"text": "Power in Demand", "font": {"size": 20}, "align": "left"},
        number = { 'font': {'size': 60, 'color': colour} },
        domain = {'x': [0, 1], 'y': [0, 1]}))

    fig.update_layout(paper_bgcolor = "#262730", height = 200,
                       margin = dict(l=30, r=30, b=0, t=0, pad=0))
    st.plotly_chart(fig, use_container_width=True)

with c3:
    fig = go.Figure(go.Indicator (
        mode = "number",
        value = st.session_state.sel_df['Power Shortage'].sum(),
        title = {"text": "Power Shortage/Excess", "font": {"size": 20}, "align": "left"},
        number = { 'font': {'size': 60, 'color': colour} },
        domain = {'x': [0, 1], 'y': [0, 1]}))

    fig.update_layout(paper_bgcolor = "#262730", height = 200,
                       margin = dict(l=30, r=30, b=0, t=0, pad=0))
    st.plotly_chart(fig, use_container_width=True)


fig = px.line(st.session_state.sel_df, x=st.session_state.sel_df.index, y=["Total Power Produced",'Power in Demand','Power Shortage'],)
fig.update_layout(paper_bgcolor = "#262730", height = 200,
                    margin = dict(l=30, r=30, b=0, t=30, pad=0))
st.plotly_chart(fig, use_container_width=True)
# css.vertival_space(10)

col1, col2, col3, col4 = st.columns(4)

df_col = ''

with col1:
    df_col = 'Megawatthours_coal'
    st.metric(label="Coal", value=st.session_state.sel_df_1[df_col][-1], delta=get_delta(df_col) )

    df_col = 'Megawatthours_petrolium'
    st.metric(label="Petrolium", value=st.session_state.sel_df_1[df_col][-1], delta=get_delta(df_col))
    
with col2:
    df_col = 'Megawatthours_hydro'
    st.metric(label="Hydro", value=st.session_state.sel_df_1[df_col][-1], delta=get_delta(df_col))
    
    df_col = 'Megawatthours_wind'
    st.metric(label="Wind", value=st.session_state.sel_df_1[df_col][-1], delta=get_delta(df_col))

with col3:
    df_col = 'Megawatthours_natural_gas'
    st.metric(label="Natural Gas", value=st.session_state.sel_df_1[df_col][-1], delta=get_delta(df_col))
    
    df_col = 'Megawatthours_solar'
    st.metric(label="Solar", value=st.session_state.sel_df_1[df_col][-1], delta=get_delta(df_col))

with col4:
    df_col = 'Megawatthours_nuclear'
    st.metric(label="Nuclear", value=st.session_state.sel_df_1[df_col][-1], delta=get_delta(df_col))
    
    df_col = 'Megawatthours_other'
    st.metric(label="Other", value=st.session_state.sel_df_1[df_col][-1], delta=get_delta(df_col))


