import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set Streamlit page configuration
st.set_page_config(page_title="AI Tool Adoption Dashboard", layout="wide")

# Title
st.title("🤖 AI Tool Adoption Dashboard")
st.markdown("Explore AI tool usage across different countries, industries, and company sizes.")

# Upload or load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('ai_adoption_dataset.csv')
    return df

df = load_data()

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔥 Top Tools",
    "🌍 By Country",
    "🏭 By Industry",
    "🏢 By Company Size"
])

# ----------- TAB 1: Top Tools -------------
with tab1:
    st.subheader("🔥 Most Used AI Tools (by Daily Active Users)")
    top_tools = df.groupby('ai_tool')['daily_active_users'].sum().reset_index().sort_values(by='daily_active_users', ascending=False)

    fig = px.bar(
        top_tools,
        x='ai_tool',
        y='daily_active_users',
        color='ai_tool',
        labels={'daily_active_users': 'Total Daily Active Users'},
        title='🔥 Most Used AI Tools (by Daily Active Users)'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ----------- TAB 2: Country-wise Analysis -------------
with tab2:
    st.subheader("🌍 Average Adoption Rate by Country per AI Tool")
    country_grp = df.groupby(['country', 'ai_tool']).agg(
        adoption_rate=('adoption_rate', 'mean'),
        count=('ai_tool', 'count')
    ).reset_index()

    fig = px.bar(
        country_grp,
        x='adoption_rate',
        y='country',
        color='country',
        animation_frame='ai_tool',
        hover_data={'count': True, 'adoption_rate': ':.2f'},
        labels={'adoption_rate': 'Adoption Rate (%)'}
    )

    fig.update_layout(
        yaxis_title="Country",
        xaxis_title="Adoption Rate (%)",
        showlegend=False,
        xaxis=dict(range=[48, 52])
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------- TAB 3: Industry-wise Analysis -------------
with tab3:
    st.subheader("🏭 AI Tool Adoption by Industry")
    industry_grp = df.groupby(['industry', 'ai_tool']).agg(
        adoption_rate=('adoption_rate', 'mean'),
        count=('ai_tool', 'count')
    ).reset_index()

    fig = px.bar(
        industry_grp,
        y='industry',
        x='adoption_rate',
        color='industry',
        animation_frame='ai_tool',
        hover_data={'count': True, 'adoption_rate': ':.2f'},
        labels={'adoption_rate': 'Adoption Rate (%)'}
    )

    fig.update_layout(
        yaxis_title="Industry",
        xaxis_title="Adoption Rate (%)",
        showlegend=False,
        xaxis=dict(range=[48, 52])
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------- TAB 4: Company Size-wise Analysis -------------
with tab4:
    st.subheader("🏢 AI Tool Adoption by Company Size")
    company_grp = df.groupby(['company_size', 'ai_tool']).agg(
        adoption_rate=('adoption_rate', 'mean'),
        count=('ai_tool', 'count')
    ).reset_index()

    fig = px.bar(
        company_grp,
        y='company_size',
        x='adoption_rate',
        color='company_size',
        animation_frame='ai_tool',
        hover_data={'count': True, 'adoption_rate': ':.2f'},
        labels={'adoption_rate': 'Adoption Rate (%)'}
    )

    fig.update_layout(
        yaxis_title="Company Size",
        xaxis_title="Adoption Rate (%)",
        showlegend=False,
        xaxis=dict(range=[48, 52])
    )
    st.plotly_chart(fig, use_container_width=True)
