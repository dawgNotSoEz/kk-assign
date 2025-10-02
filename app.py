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
    initial_sidebar_state="expanded"
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
if 'summary_length' not in st.session_state:
    st.session_state.summary_length = "3 lines"
if 'language' not in st.session_state:
    st.session_state.language = "English"

# Premium CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 2rem 0 1rem 0;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.3);
        animation: glow 3s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.4)); }
        50% { filter: drop-shadow(0 0 30px rgba(118, 75, 162, 0.6)); }
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(48, 43, 99, 0.95) 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] h2 {
        color: #667eea;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #f093fb;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(15, 12, 41, 0.4);
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.6);
        border: none;
        background: transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 12, 41, 0.6) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(15, 12, 41, 0.4);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .stRadio label {
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(15, 12, 41, 0.6) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(102, 126, 234, 0.5) !important;
        background: rgba(15, 12, 41, 0.8) !important;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        background: rgba(15, 12, 41, 0.8) !important;
        border-radius: 12px !important;
        border-left: 4px solid !important;
        padding: 1rem !important;
    }
    
    .stSuccess {
        border-left-color: #10b981 !important;
    }
    
    .stWarning {
        border-left-color: #f59e0b !important;
    }
    
    .stError {
        border-left-color: #ef4444 !important;
    }
    
    .stInfo {
        border-left-color: #3b82f6 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
        border-right-color: #764ba2 !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(15, 12, 41, 0.6) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Summary cards */
    .summary-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Animations */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main .block-container {
        animation: slideUp 0.6s ease-out;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 12, 41, 0.4);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <div style="font-size: 4rem; margin-bottom: 1rem;">📰</div>
    <h1 class="main-title">AI News Summarizer</h1>
    <p class="subtitle">Transform lengthy articles into intelligent 3-line summaries powered by AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Statistics")
    st.metric("Characters", st.session_state.char_count)
    st.metric("Words", st.session_state.word_count)
    st.metric("Summaries", len(st.session_state.history))

# Main content
tab1, tab2, tab3 = st.tabs(["🔍 Summarize", "📚 History", "⚙️ Settings"])

with tab1:
    st.subheader("Choose Input Method")
    
    input_type = st.radio(
        "Select input type",
        ["📝 Direct Text Input", "🔗 URL Link"],
        horizontal=True
    )
    
    if input_type == "📝 Direct Text Input":
        text_input = st.text_area(
            "Paste your article content:",
            height=180,
            placeholder="Copy and paste the full article text you want to summarize..."
        )
        
        if text_input:
            st.session_state.char_count = len(text_input)
            st.session_state.word_count = len(text_input.split())
        
        if st.button("✨ Generate Summary", type="primary"):
            if text_input.strip():
                with st.spinner("🤖 AI is analyzing your text..."):
                    try:
                        # Use settings from session state
                        summary = summarize_text(
                            text_input, 
                            length=st.session_state.summary_length,
                            language=st.session_state.language
                        )
                        
                        st.success("✅ Summary Generated!")
                        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                        
                        # Dynamic title based on length
                        if st.session_state.summary_length == "3 lines":
                            title = "### 📰 Your 3-Line Summary"
                            max_lines = 3
                        elif st.session_state.summary_length == "5 lines":
                            title = "### 📰 Your 5-Line Summary"
                            max_lines = 5
                        else:
                            title = "### 📰 Your Summary"
                            max_lines = 10
                        
                        st.markdown(title)
                        
                        # Show language badge if not English
                        if st.session_state.language != "English":
                            st.markdown(f'<span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 4px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; color: white; display: inline-block; margin-bottom: 1rem;">🌐 {st.session_state.language}</span>', unsafe_allow_html=True)
                        
                        lines = summary.strip().split('\n')
                        for i, line in enumerate(lines[:max_lines], 1):
                            if line.strip():
                                st.markdown(f"""
                                <div style="
                                    background: rgba(102, 126, 234, 0.1);
                                    border-left: 4px solid #667eea;
                                    padding: 12px 16px;
                                    margin: 12px 0;
                                    border-radius: 8px;
                                    font-size: 1.05rem;
                                    line-height: 1.6;
                                ">
                                    <strong style="color: #f093fb;">{i}.</strong> {line.strip()}
                                </div>
                                """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Save to history
                        st.session_state.history.append({
                            'type': 'text',
                            'input': text_input[:100] + '...',
                            'summary': summary,
                            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter some text to summarize")
    
    else:  # URL Input
        url_input = st.text_input(
            "Enter article URL:",
            placeholder="https://example.com/article"
        )
        
        if st.button("✨ Generate Summary", type="primary", key="url_btn"):
            if url_input.strip():
                with st.spinner("🤖 Fetching and analyzing article..."):
                    try:
                        # Use settings from session state
                        summary = summarize_url(
                            url_input,
                            length=st.session_state.summary_length,
                            language=st.session_state.language
                        )
                        
                        st.success("✅ Summary Generated!")
                        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
                        
                        # Dynamic title based on length
                        if st.session_state.summary_length == "3 lines":
                            title = "### 📰 Your 3-Line Summary"
                            max_lines = 3
                        elif st.session_state.summary_length == "5 lines":
                            title = "### 📰 Your 5-Line Summary"
                            max_lines = 5
                        else:
                            title = "### 📰 Your Summary"
                            max_lines = 10
                        
                        st.markdown(title)
                        
                        # Show language badge if not English
                        if st.session_state.language != "English":
                            st.markdown(f'<span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 4px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; color: white; display: inline-block; margin-bottom: 1rem;">🌐 {st.session_state.language}</span>', unsafe_allow_html=True)
                        
                        lines = summary.strip().split('\n')
                        for i, line in enumerate(lines[:max_lines], 1):
                            if line.strip():
                                st.markdown(f"""
                                <div style="
                                    background: rgba(102, 126, 234, 0.1);
                                    border-left: 4px solid #667eea;
                                    padding: 12px 16px;
                                    margin: 12px 0;
                                    border-radius: 8px;
                                    font-size: 1.05rem;
                                    line-height: 1.6;
                                ">
                                    <strong style="color: #f093fb;">{i}.</strong> {line.strip()}
                                </div>
                                """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Save to history
                        st.session_state.history.append({
                            'type': 'url',
                            'input': url_input,
                            'summary': summary,
                            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a valid URL")

with tab2:
    st.subheader("📚 Summary History")
    
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

with tab3:
    st.subheader("⚙️ Settings & Preferences")
    
    st.markdown("#### 📝 Summary Settings")
    st.info("💡 These settings will be applied to all future summaries")
    
    summary_length = st.selectbox(
        "Summary Length",
        ["3 lines", "5 lines", "1 paragraph"],
        index=["3 lines", "5 lines", "1 paragraph"].index(st.session_state.summary_length)
    )
    
    language = st.selectbox(
        "Language",
        ["English", "Spanish", "French", "German", "Hindi", "Chinese", "Japanese", "Arabic", "Portuguese", "Russian"],
        index=["English", "Spanish", "French", "German", "Hindi", "Chinese", "Japanese", "Arabic", "Portuguese", "Russian"].index(st.session_state.language) if st.session_state.language in ["English", "Spanish", "French", "German", "Hindi", "Chinese", "Japanese", "Arabic", "Portuguese", "Russian"] else 0
    )
    
    # Save settings button
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.session_state.summary_length = summary_length
        st.session_state.language = language
        st.success(f"✅ Settings saved! Summary length: {summary_length}, Language: {language}")
        st.balloons()
    
    # Show current settings
    st.markdown("#### � Current Active Settings")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Length", st.session_state.summary_length)
    with col2:
        st.metric("Language", st.session_state.language)
    
    st.markdown("#### �💾 Data Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.success("✅ History cleared!")
            st.rerun()
    with col2:
        if st.button("📊 Export History", use_container_width=True):
            if st.session_state.history:
                import json
                history_json = json.dumps(st.session_state.history, indent=2)
                st.download_button(
                    label="⬇️ Download JSON",
                    data=history_json,
                    file_name="summary_history.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ No history to export")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin: 0.5rem 0;">
        🚀 Built with <span style="color: #667eea;">Streamlit</span> & <span style="color: #764ba2;">Google Gemini AI</span>
    </p>
    <p style="color: rgba(255,255,255,0.3); font-size: 0.8rem;">
        ⚡ Powered by AI • 🔒 Privacy-focused • 🌟 Open Source
    </p>
</div>
""", unsafe_allow_html=True)
