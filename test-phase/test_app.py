import streamlit as st

st.title("Test App")
st.write("If you can see this, Streamlit is working!")

try:
    from summariser import summarize_text
    st.success("✅ Summariser imported successfully")
except Exception as e:
    st.error(f"❌ Error importing summariser: {e}")

try:
    from config import api_key
    if api_key:
        st.success("✅ API key loaded")
    else:
        st.warning("⚠️ API key is empty")
except Exception as e:
    st.error(f"❌ Error loading config: {e}")
