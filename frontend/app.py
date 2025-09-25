import streamlit as st
import requests
import os
from pathlib import Path
import time

# ADNOC Color Theme Configuration
st.set_page_config(
    page_title="TalentHC AI Assistant",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ADNOC theme
st.markdown("""
<style>
    /* ADNOC Color Theme */
    :root {
        --adnoc-teal: #4ECDC4;
        --adnoc-dark-teal: #3DB5AC;
        --adnoc-blue: #1E40AF;
        --adnoc-dark-blue: #1E3A8A;
        --adnoc-coral: #FF6B6B;
        --adnoc-yellow: #FFE66D;
        --adnoc-white: #FFFFFF;
        --adnoc-light-gray: #F8FAFC;
        --adnoc-dark-gray: #334155;
    }
    
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, var(--adnoc-teal) 0%, var(--adnoc-dark-teal) 50%, var(--adnoc-blue) 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        margin: 10px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Main content area - reduce bottom padding since text box is floating */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 60px; /* Reduced further since text box is now floating */
        background: transparent;
        max-width: none;
        width: 100%;
    }
    
    /* Header section */
    .header-container {
        display: flex;
        align-items: flex-start;
        margin-bottom: 0;
        padding: 0 2rem;
        position: relative;
    }
    
    /* Title area - centered */
    .title-section {
        flex: 1;
        text-align: center;
        padding: 0 300px; /* Space for example questions */
    }
    
    /* Title styling */
    h1 {
        color: var(--adnoc-white) !important;
        text-align: center;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 0.5rem !important;
    }
    
    /* Subtitle styling */
    .subtitle {
        color: var(--adnoc-yellow) !important;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        margin-bottom: 0 !important;
    }
    
    /* Example questions - now in proper column, not absolute */
    .example-questions {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 10px; /* Reduced from 15px */
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-top: 0 !important;
    }
    
    .example-questions h3 {
        color: var(--adnoc-blue) !important;
        text-align: center;
        margin-bottom: 10px !important;
        margin-top: 0 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 4px 8px !important;
        background: rgba(78, 205, 196, 0.1) !important;
        border-radius: 6px !important;
        border-left: 3px solid var(--adnoc-teal) !important;
    }
    
    /* ChatGPT/Claude style chat container */
    .chat-container {
        max-width: 800px;
        margin: 2rem auto 0;
        padding: 0 2rem;
    }
    
    /* Chat messages */
    .chat-message {
        margin: 20px 0;
        padding: 20px;
        border-radius: 15px;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(45deg, var(--adnoc-blue), var(--adnoc-dark-blue));
        color: white;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3);
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.95);
        color: var(--adnoc-dark-gray);
        margin-right: 20%;
        border-left: 4px solid var(--adnoc-teal);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .message-header {
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    
    .message-content {
        line-height: 1.6;
    }
    
    /* Welcome screen - adjust position to account for higher text box */
    .welcome-screen {
        max-width: 800px;
        margin: 2rem auto 6rem; /* Added bottom margin to account for higher text box */
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        padding: 0 2rem;
    }
    
    .welcome-screen h2 {
        color: var(--adnoc-white) !important;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    .welcome-screen p {
        font-size: 1.2rem !important;
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* *** REFINED INPUT CONTAINER STYLING *** */
    .chat-input-container {
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 80% !important;
        max-width: 800px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 8px !important;
        border-radius: 25px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        z-index: 999 !important;
    }

    /* Input field styling - make it seamless */
    .stTextInput label {
        display: none; /* Hide the label */
    }
    .stTextInput input {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 12px 15px !important;
        font-size: 16px !important;
        color: var(--adnoc-dark-gray) !important;
        box-shadow: none !important;
        width: 100% !important;
        outline: none !important;
    }
    
    .stTextInput input:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Hide the input container styling */
    .stTextInput > div {
        border: none !important;
        background: transparent !important;
    }
    
    /* Button styling - integrate seamlessly with input */
    .stButton button {
        background: linear-gradient(45deg, var(--adnoc-coral), var(--adnoc-yellow)) !important;
        color: white !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
        white-space: nowrap !important;
        font-size: 14px !important;
        height: auto !important;
    }
    
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Example question buttons */
    .example-questions .stButton button {
        width: 100% !important;
        margin-bottom: 8px !important;
        text-align: left !important;
        font-size: 13px !important;
        padding: 10px 15px !important;
    }
    
    /* Sidebar headers */
    .css-1d391kg h2, .css-1d391kg h3 {
        color: var(--adnoc-blue) !important;
        font-weight: 600 !important;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess {
        background: rgba(78, 205, 196, 0.1) !important;
        border: 1px solid var(--adnoc-teal) !important;
        border-radius: 10px !important;
    }
    
    .stWarning {
        background: rgba(255, 230, 109, 0.1) !important;
        border: 1px solid var(--adnoc-yellow) !important;
        border-radius: 10px !important;
    }
    
    .stError {
        background: rgba(255, 107, 107, 0.1) !important;
        border: 1px solid var(--adnoc-coral) !important;
        border-radius: 10px !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 1200px) {
        .example-questions {
            display: none;
        }
        
        .title-section {
            padding: 0;
        }
        
        .user-message, .bot-message {
            margin-left: 0;
            margin-right: 0;
        }
        
        .chat-container {
            padding: 0 1rem;
        }
    }
    
    /* Loading spinner */
    .stSpinner {
        color: var(--adnoc-teal) !important;
    }

    /* Style for the loading text container */
    .spinner-container {
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: var(--adnoc-dark-gray);
        font-size: 1rem;
        font-weight: 500;
        z-index: 998;
    }

    .stSpinner-circle {
        border-top: 2px solid var(--adnoc-teal) !important;
        border-right: 2px solid transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# Sidebar with stats
with st.sidebar:
    st.header("📊 Data Sources")
    
    # Check if scraped data exists
    scraped_dir = Path("scraped_data")
    uploads_dir = Path("uploads")
    
    if scraped_dir.exists():
        news_file = scraped_dir / "adnoc_news.json"
        company_file = scraped_dir / "adnoc_company_info.json"
        
        if news_file.exists():
            st.success("✅ ADNOC News Articles")
        if company_file.exists():
            st.success("✅ Company Information")
    else:
        st.warning("⚠️ No scraped data found")
        st.info("Run `python run_scraper.py` to collect ADNOC data")
    
    st.header("🔄 Actions")
    if st.button("🕷️ Refresh ADNOC Data"):
        st.info("Run the scraper script to update data")
    
    st.header("📈 Quick Stats")
    # Count uploaded files
    if uploads_dir.exists():
        file_count = len([f for f in uploads_dir.iterdir() if f.is_file()])
    else:
        file_count = 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", file_count)
        st.metric("Data Sources", 8)
    with col2:
        st.metric("News Articles", 150)  
        st.metric("Uptime", "99%")

# Header section with just the title
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1>🌟TalentHC AI Assistant</h1>
    <p class="subtitle">Your intelligent assistant for ADNOC information and insights</p>
</div>
""", unsafe_allow_html=True)

# Main chat area (Claude/ChatGPT style)
if st.session_state.chat:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    # Display chat history
    for i, (sender, message) in enumerate(st.session_state.chat):
        if sender == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-header">🙋 You</div>
                <div class="message-content">{message}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Check if this is a loading message
            if message == "loading":
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <div class="spinner-container">
                        <div class="stSpinner">
                            <div class="stSpinner-circle"></div>
                        </div>
                        <p style="margin-left: 10px;">🔍 Searching ADNOC knowledge base...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <div class="message-header">🤖 HC Assistant</div>
                    <div class="message-content">{message}</div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Welcome screen
    st.markdown("""
    <div class="welcome-screen">
        <h2>👋 Welcome to TalentHC Assistant!</h2>
        <p>Ask me anything about ADNOC, or click on an example question to get started.</p>
    </div>
    """, unsafe_allow_html=True)

# *** REFACTOR: Use st.form for cleaner input handling and to prevent double messages ***
with st.form(key="chat_form", clear_on_submit=True):
    # Use columns inside the form for a seamless side-by-side layout
    col1, col2 = st.columns([6, 1])
    
    with col1:
        question = st.text_input(
            "Ask me anything about ADNOC:",
            placeholder="e.g., What are ADNOC's key sustainability goals?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.form_submit_button("Send ↗", use_container_width=True)

# Handle form submission
if send_button and question:
    # Only process non-empty questions
    if question.strip():
        # Append user message and a 'loading' message to chat history
        st.session_state.chat.append(("user", question))
        st.session_state.chat.append(("bot", "loading"))
        st.session_state.is_processing = True
        
        # Rerun to show the user's message and the loading indicator immediately
        st.rerun()

# This part of the code runs after the rerun to fetch the response
if st.session_state.is_processing and st.session_state.chat[-1][1] == "loading":
    try:
        res = requests.post(
            "http://localhost:8080/ask",
            json={"question": question},
            timeout=30
        )
        
        if res.status_code == 200:
            answer = res.json().get("answer", "No answer received")
            # Replace the 'loading' message with the actual answer
            st.session_state.chat[-1] = ("bot", answer)
        else:
            st.session_state.chat[-1] = ("bot", f"Error: {res.status_code} - {res.text}")
            
    except requests.exceptions.ConnectionError:
        st.session_state.chat[-1] = ("bot", "❌ Cannot connect to backend. Make sure the API server is running on port 8080")
    except requests.exceptions.Timeout:
        st.session_state.chat[-1] = ("bot", "⏱️ Request timed out. The query might be too complex.")
    except Exception as e:
        st.session_state.chat[-1] = ("bot", f"❌ Error: {str(e)}")
    
    st.session_state.is_processing = False
    
    # Rerun again to display the final answer
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: rgba(255, 255, 255, 0.8); margin-top: 2rem;'>
        <small>TalentHC AI Assistant - Powered by ADNOC NextWave Program</small>
    </div>
    """, 
    unsafe_allow_html=True
)
