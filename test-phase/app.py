import streamlit as st
import time
from summariser import summarize_text, summarize_url
import requests
from bs4 import BeautifulSoup

# Page configuration
st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'char_count' not in st.session_state:
    st.session_state.char_count = 0
if 'word_count' not in st.session_state:
    st.session_state.word_count = 0
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Summarize"

# Custom CSS for premium design
def load_premium_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Background - Premium Dark Theme */
    .stApp {
        background: #1a1a2e;
        font-family: 'Inter', sans-serif;
        animation: fadeIn 0.8s ease-in;
        position: relative;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, 
            rgba(26,26,46,1) 0%, 
            rgba(16,16,34,1) 50%, 
            rgba(26,26,46,1) 100%
        );
        opacity: 0.5;
        pointer-events: none;
        z-index: 0;
    }

    /* Remove default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Main Container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        animation: slideUp 0.6s ease-out 0.2s both;
        position: relative;
        z-index: 1;
    }

    /* Hero Section */
    .header-section {
        text-align: center;
        padding: 4rem 0 3rem 0;
        position: relative;
        margin-bottom: 2rem;
    }

    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 600px;
        height: 400px;
        background: radial-gradient(circle, rgba(232,205,126,0.15) 0%, transparent 70%);
        filter: blur(80px);
        pointer-events: none;
        z-index: -1;
    }

    .newspaper-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        background: linear-gradient(135deg, #E8CD7E 0%, #FFB244 50%, #9E4700 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 4px 20px rgba(232,205,126,0.3));
        animation: float 3s ease-in-out infinite;
    }

    .header-title {
        font-size: 4.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1.1;
        animation: slideUp 0.8s ease-out 0.4s both;
        text-shadow: 0 0 40px rgba(232,205,126,0.3);
    }

    .header-title span {
        background: linear-gradient(135deg, #E8CD7E 0%, #FFB244 50%, #9E4700 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .header-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
        animation: slideUp 0.8s ease-out 0.6s both;
    }

    /* Modern Glass Cards */
    .glass-card {
        background: rgba(40, 40, 60, 0.8);
        backdrop-filter: blur(30px) saturate(180%);
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        border: 1px solid rgba(232, 205, 126, 0.2);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent 0%,
            rgba(232,205,126,0.5) 30%,
            rgba(255,178,68,0.5) 50%,
            rgba(232,205,126,0.5) 70%,
            transparent 100%
        );
        opacity: 0.6;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(232, 205, 126, 0.2);
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.5),
            0 0 20px rgba(232,205,126,0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    /* Premium Sidebar Styling */
    .sidebar-overlay {
        background: linear-gradient(135deg, rgba(232,205,126,0.08), rgba(255,178,68,0.05));
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(232, 205, 126, 0.15);
        box-shadow: 
            0 8px 24px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .sidebar-overlay h3 {
        background: linear-gradient(135deg, #E8CD7E 0%, #FFB244 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    .sidebar-section {
        background: rgba(30, 30, 40, 0.4);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(232, 205, 126, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .sidebar-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent,
            rgba(232,205,126,0.3),
            transparent
        );
    }

    .sidebar-section h3 {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .sidebar-section.active {
        border-color: rgba(232, 205, 126, 0.3);
        background: rgba(30, 30, 40, 0.6);
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.2),
            0 0 20px rgba(232,205,126,0.1);
    }

    .sidebar-section:hover {
        border-color: rgba(232, 205, 126, 0.2);
        transform: translateX(2px);
    }

    /* Premium Statistics */
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #E8CD7E 0%, #FFB244 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'JetBrains Mono', monospace;
        filter: drop-shadow(0 0 20px rgba(232,205,126,0.3));
        margin-bottom: 0.5rem;
    }

    .stat-label {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* Modern Example Buttons */
    .example-btn {
        background: rgba(30, 30, 40, 0.3);
        border: 1px solid rgba(91, 129, 131, 0.2);
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        margin: 0.6rem 0;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: rgba(255, 255, 255, 0.8);
        text-align: left;
        width: 100%;
        font-size: 0.9rem;
        font-weight: 500;
        position: relative;
        overflow: hidden;
    }

    .example-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent,
            rgba(232,205,126,0.1),
            transparent
        );
        transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .example-btn:hover {
        background: rgba(30, 30, 40, 0.6);
        border-color: rgba(232, 205, 126, 0.4);
        color: #FFB244;
        transform: translateX(4px);
        box-shadow: 0 4px 16px rgba(232,205,126,0.15);
    }

    .example-btn:hover::before {
        left: 100%;
    }

    /* Modern Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(20, 20, 30, 0.5) !important;
        border: 1px solid rgba(91, 129, 131, 0.3) !important;
        border-radius: 16px !important;
        padding: 1rem 1.5rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.3) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        outline: none !important;
        border: 1px solid rgba(232, 205, 126, 0.6) !important;
        background: rgba(20, 20, 30, 0.7) !important;
        box-shadow: 
            0 0 0 3px rgba(232, 205, 126, 0.1),
            0 4px 20px rgba(232,205,126,0.2) !important;
    }

    /* Premium Radio Buttons */
    .stRadio > div {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        background: rgba(20, 20, 30, 0.3);
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid rgba(91, 129, 131, 0.2);
    }

    .stRadio > div > label {
        background: transparent;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
        text-align: center;
        flex: 1;
        color: rgba(255, 255, 255, 0.6);
        position: relative;
    }

    .stRadio > div > label:hover {
        background: rgba(30, 30, 40, 0.5);
        color: rgba(255, 255, 255, 0.9);
    }

    .stRadio > div > label[data-selected="true"] {
        background: linear-gradient(135deg, rgba(232,205,126,0.2), rgba(255,178,68,0.2));
        border: 1px solid rgba(232, 205, 126, 0.4);
        color: #FFB244;
        box-shadow: 
            0 4px 16px rgba(232,205,126,0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    /* Premium Primary Buttons */
    .stButton > button[kind="primary"],
    .stButton > button {
        background: linear-gradient(135deg, #E8CD7E 0%, #FFB244 50%, #9E4700 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        width: 100% !important;
        margin-top: 1.5rem !important;
        box-shadow: 
            0 4px 20px rgba(232,205,126,0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent,
            rgba(255,255,255,0.3),
            transparent
        );
        transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 8px 32px rgba(232,205,126,0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Premium Loading Animation */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        flex-direction: column;
        gap: 1.5rem;
    }

    .loading-gradient {
        width: 64px;
        height: 64px;
        border: 3px solid transparent;
        border-top: 3px solid #E8CD7E;
        border-right: 3px solid #FFB244;
        border-bottom: 3px solid #9E4700;
        border-radius: 50%;
        animation: spin 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        box-shadow: 0 0 30px rgba(232,205,126,0.3);
    }

    .loading-container p {
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
    }

    /* Premium Summary Display */
    .summary-card {
        background: rgba(40, 40, 60, 0.9);
        backdrop-filter: blur(30px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(232, 205, 126, 0.3);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.5),
            0 0 30px rgba(232,205,126,0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }

    .summary-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent,
            rgba(232,205,126,0.6),
            rgba(255,178,68,0.6),
            rgba(232,205,126,0.6),
            transparent
        );
    }

    .summary-card h3 {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .summary-line {
        background: rgba(30, 30, 40, 0.5);
        border-radius: 16px;
        padding: 1.5rem 1.5rem 1.5rem 0;
        margin: 1.2rem 0;
        border-left: 3px solid rgba(232, 205, 126, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }

    .summary-line:hover {
        background: rgba(30, 30, 40, 0.7);
        border-left-color: rgba(255, 178, 68, 0.6);
        transform: translateX(8px);
        box-shadow: 0 4px 16px rgba(232,205,126,0.15);
    }

    .line-number {
        background: linear-gradient(135deg, #E8CD7E 0%, #FFB244 100%);
        color: #000000;
        border-radius: 12px;
        min-width: 40px;
        height: 40px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.1rem;
        font-family: 'JetBrains Mono', monospace;
        margin-left: 1.5rem;
        box-shadow: 
            0 4px 12px rgba(232,205,126,0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .summary-line span:last-child {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.7;
        flex: 1;
    }

    /* Action Buttons */
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 2.5rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        flex-wrap: wrap;
    }

    .action-buttons .stButton > button {
        background: rgba(30, 30, 40, 0.6) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(91, 129, 131, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.5rem !important;
        font-weight: 500 !important;
        margin-top: 0 !important;
    }

    .action-buttons .stButton > button:hover {
        background: rgba(30, 30, 40, 0.8) !important;
        border-color: rgba(232, 205, 126, 0.5) !important;
        color: #FFB244 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(232,205,126,0.2) !important;
    }

    /* Article Preview */
    .preview-section {
        background: rgba(30, 30, 40, 0.4);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 3px solid rgba(91, 129, 131, 0.5);
        border: 1px solid rgba(91, 129, 131, 0.2);
    }

    .preview-title {
        font-weight: 600;
        color: #FFB244;
        margin-bottom: 0.8rem;
        font-size: 1rem;
    }

    .preview-text {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* Custom Tabs */
    .custom-tabs {
        display: flex;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 0.5rem;
        margin: 2rem 0 1rem 0;
        backdrop-filter: blur(10px);
    }

    .tab-button {
        flex: 1;
        padding: 1rem 1.5rem;
        border: none;
        background: transparent;
        border-radius: 12px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        color: rgba(77, 80, 192, 0.7);
    }

    .tab-button.active {
        background: linear-gradient(135deg, rgba(142, 208, 212, 0.8), rgba(77, 80, 192, 0.8));
        color: white;
        box-shadow: 0 4px 15px rgba(77, 80, 192, 0.3);
    }

    /* Premium Footer */
    .footer {
        background: rgba(20, 20, 30, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin-top: 5rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(232, 205, 126, 0.15);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent,
            rgba(232,205,126,0.4),
            rgba(255,178,68,0.4),
            rgba(232,205,126,0.4),
            transparent
        );
    }

    .footer-links {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }

    .footer-link {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.7rem 1.2rem;
        border-radius: 12px;
        background: rgba(30, 30, 40, 0.4);
        border: 1px solid rgba(91, 129, 131, 0.2);
        font-weight: 500;
    }

    .footer-link:hover {
        color: #FFB244;
        background: rgba(30, 30, 40, 0.6);
        border-color: rgba(232, 205, 126, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(232,205,126,0.2);
    }

    .footer-brand {
        background: linear-gradient(135deg, #E8CD7E 0%, #FFB244 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin: 0.5rem 0;
        filter: drop-shadow(0 0 20px rgba(232,205,126,0.3));
    }

    /* Enhanced Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
        }
        50% {
            transform: scale(1.05);
            filter: drop-shadow(4px 4px 8px rgba(0,0,0,0.4));
        }
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes gradientShift {
        0%, 100% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
    }

    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }

    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(142, 208, 212, 0.3);
        }
        50% {
            box-shadow: 0 0 30px rgba(142, 208, 212, 0.6), 0 0 40px rgba(142, 208, 212, 0.4);
        }
    }

    /* Tab Buttons Styling */
    .stButton > button[data-testid="baseButton-secondary"] {
        background: rgba(30, 30, 40, 0.5) !important;
        color: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(91, 129, 131, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background: rgba(30, 30, 40, 0.7) !important;
        border-color: rgba(232, 205, 126, 0.4) !important;
        color: #FFB244 !important;
        transform: translateY(-1px) !important;
    }

    /* Expander styling */
    .stExpander {
        background: rgba(20, 20, 30, 0.4) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(91, 129, 131, 0.2) !important;
        margin: 1rem 0 !important;
    }

    .stExpander summary {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(20, 20, 30, 0.5) !important;
        border: 1px solid rgba(91, 129, 131, 0.3) !important;
        border-radius: 12px !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }

    /* Success/Info/Warning messages */
    .stSuccess, .stInfo, .stWarning {
        background: rgba(20, 20, 30, 0.6) !important;
        border-radius: 12px !important;
        border-left: 3px solid rgba(232, 205, 126, 0.6) !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }

    /* Mobile Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem;
        }

        .glass-card {
            padding: 1.5rem;
        }

        .main-container {
            padding: 0 1rem;
        }

        .action-buttons {
            flex-direction: column;
        }

        .footer-links {
            flex-direction: column;
            gap: 1rem;
        }

        .stRadio > div {
            flex-direction: column;
        }
    }

    /* Dark theme toggle styles */
    .theme-toggle-btn {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(142, 208, 212, 0.3);
        border-radius: 50px;
        padding: 0.8rem 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        color: rgba(18, 0, 142, 1.000);
        font-weight: 500;
        margin: 1rem 0;
    }

    .theme-toggle-btn:hover {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(77, 80, 192, 0.4);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

load_premium_css()

# Sidebar Content
with st.sidebar:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # App Description Card
    st.markdown("""
    <div class="sidebar-overlay">
        <h3 style="color: white; margin-bottom: 1rem; text-align: center;">🚀 AI News Summarizer</h3>
        <p style="color: rgba(255,255,255,0.9); text-align: center; line-height: 1.5;">
            Transform lengthy articles into concise 3-line summaries using advanced AI technology.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Statistics Section
    st.markdown('<div class="sidebar-section active">', unsafe_allow_html=True)
    st.markdown("### 📊 Live Statistics")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stat-value">{st.session_state.char_count:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Characters</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="stat-value">{st.session_state.word_count:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Words</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Example URLs
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🔗 Try These Examples")

    example_urls = [
        "https://www.bbc.com/news",
        "https://www.reuters.com/world/",
        "https://techcrunch.com/",
        "https://www.cnn.com/world"
    ]

    for url in example_urls:
        site_name = url.split('//')[1].split('/')[0]
        if st.button(f"📰 {site_name}", key=url, help=f"Load {site_name}"):
            st.session_state.example_url = url

    st.markdown('</div>', unsafe_allow_html=True)

    # Theme Toggle
    if st.button("🌓 Toggle Theme", key="theme_toggle", help="Switch between light and dark themes"):
        # Theme toggle functionality will be handled in main content
        pass

    st.markdown('</div>', unsafe_allow_html=True)

# Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-section">
    <div class="newspaper-icon">📰</div>
    <h1 class="header-title">AI News <span>Summarizer</span></h1>
    <p class="header-subtitle">Transform lengthy articles into intelligent 3-line summaries in seconds</p>
</div>
""", unsafe_allow_html=True)

# Custom Tabs Implementation
col1, col2, col3 = st.columns(3)

tab_names = ["🔍 Summarize", "📚 History", "⚙️ Settings"]
tab_keys = ["summarize_tab", "history_tab", "settings_tab"]

with col1:
    if st.button(tab_names[0], key=tab_keys[0], use_container_width=True,
                 help="Create new summaries"):
        st.session_state.current_tab = "Summarize"

with col2:
    if st.button(tab_names[1], key=tab_keys[1], use_container_width=True,
                 help="View summary history"):
        st.session_state.current_tab = "History"

with col3:
    if st.button(tab_names[2], key=tab_keys[2], use_container_width=True,
                 help="App settings and preferences"):
        st.session_state.current_tab = "Settings"

# Content based on selected tab
if st.session_state.current_tab == "Summarize":
    # Input Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    # Radio button selection
    st.markdown("### Choose Input Method")

    input_type = st.radio(
        "Select input type",
        ["📝 Direct Text Input", "🔗 URL Link"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if input_type == "📝 Direct Text Input":
        text_input = st.text_area(
            "Paste your article content:",
            height=180,
            placeholder="Copy and paste the full article text you want to summarize...",
            key="text_input"
        )

        if text_input:
            st.session_state.char_count = len(text_input)
            st.session_state.word_count = len(text_input.split())

        if st.button("✨ Generate Summary", key="summarize_text"):
            if text_input.strip():
                # Create placeholders for dynamic content
                loading_container = st.empty()
                summary_container = st.empty()

                with loading_container:
                    st.markdown('<div class="loading-container">', unsafe_allow_html=True)
                    st.markdown('<div class="loading-gradient"></div>', unsafe_allow_html=True)
                    st.markdown('<p style="color: rgba(77,80,192,0.8); margin-top: 1rem;">🤖 AI is analyzing your text...</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Simulate loading
                time.sleep(1.5)

                try:
                    summary = summarize_text(text_input)

                    # Clear loading animation
                    loading_container.empty()

                    # Add to history
                    st.session_state.history.append({
                        'type': 'text',
                        'input': text_input[:100] + '...' if len(text_input) > 100 else text_input,
                        'summary': summary,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                    })

                    # Display summary with enhanced styling
                    with summary_container:
                        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                        st.markdown("### 📋 Your 3-Line Summary")

                        lines = summary.split('\n')
                        for i, line in enumerate(lines[:3], 1):
                            if line.strip():
                                st.markdown(f"""
                                <div class="summary-line">
                                    <span class="line-number">{i}</span>
                                    <span style="color: rgba(18,0,142,0.9); line-height: 1.6; font-weight: 500;">{line.strip()}</span>
                                </div>
                                """, unsafe_allow_html=True)

                        # Enhanced action buttons
                        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            if st.button("📋 Copy Summary", key="copy_text", use_container_width=True):
                                st.success("✅ Summary copied to clipboard!")
                        with col_b:
                            if st.button("🔄 Generate Again", key="regenerate_text", use_container_width=True):
                                st.rerun()
                        with col_c:
                            if st.button("💾 Save to History", key="save_text", use_container_width=True):
                                st.success("✅ Saved to history!")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    # Clear loading animation on error
                    loading_container.empty()
                    st.error(f"❌ Error generating summary: {str(e)}")

        else:
                st.warning("⚠️ Please enter some text to summarize")

    else:  # URL Input
        url_input = st.text_input(
            "Enter article URL:",
            placeholder="https://example.com/article",
            value=st.session_state.get('example_url', ''),
            key="url_input"
        )

        # Article Preview
        if url_input and url_input.startswith('http'):
            try:
                with st.expander("🔍 Article Preview", expanded=False):
                    st.markdown('<div class="preview-section">', unsafe_allow_html=True)

                    # Fetch article info
                    response = requests.get(url_input, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    title = soup.find('title')
                    if title:
                        st.markdown(f'<div class="preview-title">{title.get_text()}</div>', unsafe_allow_html=True)

                    # Get first paragraph
                    paragraphs = soup.find_all('p')
                    if paragraphs:
                        preview_text = paragraphs[0].get_text()[:250] + "..."
                        st.markdown(f'<div class="preview-text">{preview_text}</div>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.info("📄 Preview unavailable - article may be behind paywall or require JavaScript")

        if st.button("🌐 Summarize URL", key="summarize_url"):
            if url_input.strip():
                # Create placeholders for dynamic content
                loading_container = st.empty()
                summary_container = st.empty()

                with loading_container:
                    st.markdown('<div class="loading-container">', unsafe_allow_html=True)
                    st.markdown('<div class="loading-gradient"></div>', unsafe_allow_html=True)
                    st.markdown('<p style="color: rgba(77,80,192,0.8); margin-top: 1rem;">🔍 Fetching and analyzing article...</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Simulate loading
                time.sleep(2)

                try:
                    summary = summarize_url(url_input)

                    # Clear loading animation
                    loading_container.empty()

                    # Add to history
                    st.session_state.history.append({
                        'type': 'url',
                        'input': url_input,
                        'summary': summary,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                    })

                    # Display summary with enhanced styling
                    with summary_container:
                        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                        st.markdown("### 📋 Your 3-Line Summary")

                        lines = summary.split('\n')
                        for i, line in enumerate(lines[:3], 1):
                            if line.strip():
                                st.markdown(f"""
                                <div class="summary-line">
                                    <span class="line-number">{i}</span>
                                    <span style="color: rgba(18,0,142,0.9); line-height: 1.6; font-weight: 500;">{line.strip()}</span>
                                </div>
                                """, unsafe_allow_html=True)

                        # Enhanced action buttons
                        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            if st.button("📋 Copy Summary", key="copy_url", use_container_width=True):
                                st.success("✅ Summary copied to clipboard!")
                        with col_b:
                            if st.button("🔗 Share URL", key="share_url", use_container_width=True):
                                st.info("🔗 Share functionality coming soon!")
                        with col_c:
                            if st.button("💾 Save to History", key="save_url", use_container_width=True):
                                st.success("✅ Saved to history!")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    # Clear loading animation on error
                    loading_container.empty()
                    st.error(f"❌ Error processing URL: {str(e)}")

            else:
                st.warning("⚠️ Please enter a valid URL")

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_tab == "History":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📚 Summary History")

    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"📄 {item['type'].title()} - {item['timestamp']}", expanded=False):
                st.markdown(f"**Input:** {item['input']}")
                st.markdown(f"**Summary:** {item['summary']}")

                if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                    st.session_state.history.pop(len(st.session_state.history) - 1 - i)
                    st.rerun()
    else:
        st.info("📝 No summaries yet. Create your first summary!")

    st.markdown('</div>', unsafe_allow_html=True)

else:  # Settings tab
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings & Preferences")

    # Appearance Settings
    st.markdown("#### 🎨 Theme & Appearance")
    st.markdown("Theme toggle available in sidebar")

    # Summary Settings
    st.markdown("#### 📝 Summary Settings")
    summary_length = st.selectbox("Summary Length", ["3 lines", "5 lines", "1 paragraph"])
    language = st.selectbox("Language", ["English", "Spanish", "French", "German"])

    # Data Management
    st.markdown("#### 💾 Data Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.success("✅ History cleared!")
    with col2:
        if st.button("📊 Export History", use_container_width=True):
            st.info("📁 Export functionality coming soon!")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-links">
        <a href="https://github.com/yourusername/news-summarizer" class="footer-link" target="_blank">
            <span>💻</span> View on GitHub
        </a>
        <a href="#" class="footer-link">
            <span>📖</span> Documentation
        </a>
        <a href="#" class="footer-link">
            <span>🛠️</span> API
        </a>
    </div>
    <p class="footer-brand" style="margin: 1rem 0 0.5rem 0; font-size: 1.2rem;">
        🚀 Built with Streamlit & Google Gemini AI
    </p>
    <p style="font-size: 0.9rem; opacity: 0.7;">
        ⚡ Powered by AI • 🔒 Privacy-focused • 🌟 Open Source
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
