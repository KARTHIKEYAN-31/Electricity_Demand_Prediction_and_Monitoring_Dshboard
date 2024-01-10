import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import import_data as data
import functions as fun


st.set_page_config(
    page_title="What Happened?",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'full_df' not in st.session_state:
    st.session_state['full_df'] = None


st.header('What Happened?')

st.session_state.full_df = data.final_df.copy()
st.session_state.full_df['Total Power Produced'] = st.session_state.full_df.apply(lambda row: row.sum(), axis=1)

st.session_state.demand = data.demand.copy()

st.session_state.full_df['Power in Demand'] = st.session_state.demand['megawatthours'].values
st.session_state.full_df['Shortage'] = st.session_state.full_df['Total Power Produced'] - st.session_state.full_df['Power in Demand']

# fence = fun.get_fence(st.session_state.full_df['Shortage'])

# fig = px.box(st.session_state.full_df, y="Shortage",template='plotly_dark')
# fig.update_layout(paper_bgcolor = "#262730")
# st.plotly_chart(fig)

fig = px.line(st.session_state.full_df[['Total Power Produced','Power in Demand']],template='plotly_dark',
              color_discrete_sequence = ['green','red'])
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(paper_bgcolor = "#262730")


dummy = st.session_state.full_df.groupby(st.session_state.full_df.index.date).sum()
fence = fun.get_fence(dummy['Shortage'])

neg_fill_x0 = []
neg_fill_x1 = []
pos_fill_x0 = []
pos_fill_x1 = []
c = 0
for i, row in dummy.iterrows():
    if c == 0:
        if row['Shortage'] < fence[0]:
            c = 1
            neg_fill_x0.append(i)
            continue
        if row['Shortage'] > fence[1]:
            c = 1
            pos_fill_x0.append(i)
    else:
        if row['Shortage'] > (fence[0])and row['Shortage'] < (fence[1]):
            if len(neg_fill_x0) != len(neg_fill_x1):
                neg_fill_x1.append(i)
            if len(pos_fill_x0) != len(pos_fill_x1):
                pos_fill_x1.append(i)
            c = 0
        
if c == 1:
    if len(neg_fill_x0) != len(neg_fill_x1):
        neg_fill_x1.append(i)
    if len(pos_fill_x0) != len(pos_fill_x1):
        pos_fill_x1.append(i)



for i in range(0, len(neg_fill_x0)):
    fig.add_vrect(
        x0 = neg_fill_x0[i],
        x1 = neg_fill_x1[i],
        fillcolor = 'red',
        opacity = 0.2,
        layer = "below",
        line_width = 0
    )

for i in range(0, len(pos_fill_x0)):
    fig.add_vrect(
        x0 = pos_fill_x0[i],
        x1 = pos_fill_x1[i],
        fillcolor = 'green',
        opacity = 0.2,
        layer = "below",
        line_width = 0
    )

st.plotly_chart(fig, use_container_width=True)

with st.expander('Change in Production'):
    change_in_demand = pd.DataFrame()
    change_in_demand['Impact'] = ['Negative'for i in range(len(neg_fill_x0))] + [ 'Positive'for i in range(len(pos_fill_x0))]
    change_in_demand['Start_Date'] = neg_fill_x0 + pos_fill_x0
    change_in_demand['End_Date'] = neg_fill_x1 + pos_fill_x1
    change_in_demand['Interval'] = [ed - sd for sd,ed in zip(change_in_demand['Start_Date'],change_in_demand['End_Date'])]
    change_in_demand['Shortage/Extra_Value'] = [st.session_state.full_df[i:j]['Shortage'].sum() for i,j in zip(change_in_demand['Start_Date'],change_in_demand['End_Date'])]
    change_in_demand['Value_per_Day'] = [change_in_demand['Shortage/Extra_Value'][i]/change_in_demand['Interval'][i].days for i in range(len(change_in_demand))]

    st.dataframe(change_in_demand.sort_values('Interval', ascending=False).head(), use_container_width=True)


