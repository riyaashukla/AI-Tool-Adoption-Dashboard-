import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# Page Setup
st.set_page_config(page_title="🎮 AI Tool Gaming Dashboard", layout="wide", page_icon="🕹️")

# ---------------- CSS and Fonts ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Press+Start+2P&display=swap');
    body {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .css-18e3th9 {
        background: linear-gradient(to right, #2c003e, #3b0066);
        font-family: 'Orbitron', sans-serif;
        font-size: 22px;
    }
    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive;
        color: #39ff14;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- Voice Welcome ----------------
components.html("""
    <script>
        const msg = new SpeechSynthesisUtterance("Welcome Commander. Initializing AI Tool Adoption Dashboard.");
        msg.pitch = 1.1;
        msg.rate = 0.9;
        msg.volume = 1;
        msg.voice = speechSynthesis.getVoices().find(v => v.name.includes("Daniel") || v.name.includes("Google UK English Male"));
        setTimeout(() => speechSynthesis.speak(msg), 1000);
    </script>
""", height=0)

# ---------------- Title ----------------
st.title("🎮 AI Tool Adoption Dashboard")
st.markdown("**Choose a section to explore detailed AI analytics with voice narration.**")

# ---------------- Voice Narrator Dropdown ----------------
section = st.selectbox("🎧 Select a section:", [
    "Select One", "🎯 Top Tools", "🌐 By Country", "🏭 By Industry", "🏢 By Company Size"
])

# ---------------- Section Descriptions ----------------
descriptions = {
    "🎯 Top Tools": "This section displays the most used AI tools based on daily active users. It shows which tools are leading the adoption globally.",
    "🌐 By Country": "Here we analyze AI tool adoption across different countries. You can see how each AI tool performs geographically.",
    "🏭 By Industry": "This section shows the adoption rate of AI tools in different industries such as healthcare, finance, and education.",
    "🏢 By Company Size": "This part explores how companies of various sizes, from startups to enterprises, are adopting AI tools."
}

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    return pd.read_csv('ai_adoption_dataset.csv')

df = load_data()

# ---------------- Chart Styling ----------------
def style_futuristic(fig, x_range=None):
    fig.update_layout(
        template='plotly_dark',
        showlegend=False,
        plot_bgcolor='#000000',
        paper_bgcolor='#0f0f23',
        title_font=dict(size=24, family='Orbitron', color="#00ffff"),
        font=dict(color='#00ffcc', size=14),
        xaxis=dict(gridcolor='#3f3f3f'),
        yaxis=dict(gridcolor='#3f3f3f')
    )
    if x_range:
        fig.update_layout(xaxis=dict(range=x_range))
    if fig.layout.updatemenus:
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1500
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 600
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['easing'] = "cubic-in-out"
    return fig

# ---------------- Conditional Display Based on User Choice ----------------
if section != "Select One":
    # Voice Narration
    components.html(f"""
        <script>
            const msg = new SpeechSynthesisUtterance("{descriptions[section]}");
            msg.pitch = 1.1;
            msg.rate = 0.9;
            msg.volume = 1;
            msg.voice = speechSynthesis.getVoices().find(v => v.name.includes("Daniel") || v.name.includes("Google UK English Male"));
            speechSynthesis.speak(msg);
        </script>
    """, height=0)

    st.markdown(f"### 🧠 {descriptions[section]}")

    # Show Chart
    if section == "🎯 Top Tools":
        top_tools = df.groupby('ai_tool')['daily_active_users'].sum().reset_index().sort_values(by='daily_active_users', ascending=False)
        fig = px.bar(top_tools, x='ai_tool', y='daily_active_users', color='ai_tool', title="🏆 Most Used AI Tools")
        fig = style_futuristic(fig)
        st.plotly_chart(fig, use_container_width=True)

    elif section == "🌐 By Country":
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
            title="🌍 AI Tool Usage by Country"
        )
        fig = style_futuristic(fig, x_range=[48, 52])
        st.plotly_chart(fig, use_container_width=True)

    elif section == "🏭 By Industry":
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
            title="⚙️ AI Tools in Industry"
        )
        fig = style_futuristic(fig, x_range=[48, 52])
        st.plotly_chart(fig, use_container_width=True)

    elif section == "🏢 By Company Size":
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
            title="🏙️ AI Tools by Company Size"
        )
        fig = style_futuristic(fig, x_range=[48, 52])
        st.plotly_chart(fig, use_container_width=True)
