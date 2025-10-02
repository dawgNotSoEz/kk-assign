import streamlit as st
import traceback

st.title("Debug Mode")

try:
    # Try importing the modules
    st.write("Importing modules...")
    from summariser import summarize_text, summarize_url
    st.success("✅ Summariser imported")
    
    import requests
    from bs4 import BeautifulSoup
    st.success("✅ Requests and BeautifulSoup imported")
    
    # Try loading the CSS function
    st.write("Loading CSS...")
    exec(open('app.py').read().split('load_premium_css()')[0])
    st.success("✅ CSS loaded")
    
    st.write("All imports successful! The issue must be in the app execution.")
    
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.code(traceback.format_exc())
