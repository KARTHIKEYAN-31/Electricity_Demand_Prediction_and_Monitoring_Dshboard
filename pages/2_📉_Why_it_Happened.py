import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import import_data as data


st.set_page_config(
    page_title="Why it Happened",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="collapsed"
)


if 'full_df' not in st.session_state:
    st.session_state['full_df'] = None



st.header('Why it Happened?')


st.session_state.full_df = data.final_df.copy()
st.session_state.full_df['Total Power Produced'] = st.session_state.full_df.apply(lambda row: row.sum(), axis=1)

st.session_state.demand = data.demand.copy()

st.session_state.full_df['Power in Demand'] = st.session_state.demand['megawatthours'].values
st.session_state.full_df['Shortage'] = st.session_state.full_df['Total Power Produced'] - st.session_state.full_df['Power in Demand']


sb = st.sidebar.selectbox('Select Feature to Analyze', ['Demand','Coal','Natural Gas','Nuclear','Hydroelectric',
        'Solar','Wind','Other','Shortage'] )

# if sb == 'Demand':





