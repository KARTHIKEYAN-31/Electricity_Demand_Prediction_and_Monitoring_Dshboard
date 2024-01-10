import streamlit as st

def css():
    st.set_page_config(layout="wide",
        page_title="Home",
        page_icon="📊",
        initial_sidebar_state = "collapsed")
    

        # center metric value
    st.markdown(
        """
        <style>
        [data-testid="stMetricValue"] > div:nth-child(1) {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        [data-testid="stMetric"]{
            align-items: center;
            background-color: #262730;
            padding: 10px;
            padding-top: 30px;
            padding-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        [data-testid="stMetricLabel"]{
            align-items: center;
            position: relative;
            padding: 10px;
            padding-top: 0px;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        [data-testid="stMetricDelta"]{
            align-items: center;
            padding: 10px;
            padding-bottom: 0px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )





def vertival_space(x):
    st.markdown("""
    <style>
        .vertical-space {{
            height: {}px;
        }}
    </style>
    """.format(x), 
    unsafe_allow_html=True)
    st.markdown('<div class="vertical-space"></div>', unsafe_allow_html=True)