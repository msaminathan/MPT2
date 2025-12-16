
import streamlit as st

st.set_page_config(page_title="Built with Antigravity", page_icon="🚀", layout="wide")

# Custom CSS (consistent with other pages)
st.markdown("""
<style>
    .stAppHeader { background: linear-gradient(90deg, #1E1E2E 0%, #2D2B55 100%); }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #7aa2f7, #99c0d9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card {
        background-color: #2D2B55;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #414868;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Built with Antigravity")

st.markdown("""
### The Making of this App
This entire application was built using **Antigravity**, an advanced AI agentic coding assistant developed by Google Deepmind. 
It demonstrates how human intent can be rapidly translated into sophisticated software through collaboration with an intelligent agent.
""")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🤖 The Agent's Role")
    st.write("""
    Antigravity acted as an autonomous pair programmer, handling the entire development lifecycle:
    
    *   **Architecture**: Designed the multi-page structure of the Streamlit application.
    *   **Core Logic**: Implemented complex financial algorithms (Efficient Frontier, Sharpe Ratio, Monte Carlo simulations) in Python.
    *   **UI/UX Design**: Crafted the "dark mode" aesthetic, responsiveness, and interactive visualizations using Plotly.
    *   **Debugging**: Proactively identified and fixed issues, such as handling delisted tickers in the Energy sector data.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("✨ Key Capabilities Demonstrated")
    st.write("""
    *   **Tool Usage**: The agent used terminal commands, file editors, and search tools to navigate and modify the codebase.
    *   **Context Awareness**: Understood the domain of Modern Portfolio Theory to create relevant educational content and functional tools.
    *   **Iterative Refinement**: Responded to user feedback to add features (like this page!) and refine the user experience.
    *   **Self-Correction**: Detected errors during execution and self-corrected without needing explicit instructions for every fix.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.subheader("🛠️ Development Workflow")
st.code("""
1. User Request: "Build a Modern Portfolio Theory app with these features..."
2. Agent Planning: Antigravity analyzed requirements and planned the file structure.
3. Execution: The agent wrote the code for:
    - utils.py (Financial calculations)
    - Home.py (Landing page)
    - Market Explorer, Portfolio Optimizer, etc.
4. Refinement: Agent iteratively polished the UI and fixed bugs (e.g., equation rendering, data fetching).
""", language="markdown")

st.info("Antigravity allows developers to focus on the *what* and *why*, while it handles the *how*.")
