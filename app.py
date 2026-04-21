import streamlit as st
from datetime import datetime, date, time, timedelta
from st_gsheets_connection import GSheetsConnection  # Updated import
import pandas as pd

# Set up page config
st.set_page_config(page_title="J95 GENERIS PRODUCTION", page_icon="🎙️", layout="centered")

# --- CLEAN CYBERPUNK CSS ---
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { color: #00ffcc; }
    h1, h2, h3 { color: #ff00ff !important; text-shadow: 2px 2px #000000; }
    .stButton>button {
        background-color: #ff00ff;
        color: white;
        border-radius: 10px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
# Ensure your secrets.toml has [connections.gsheets]
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Connection link pending. Check Streamlit Secrets.")

# --- BRANDING HEADER ---
st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #ff00ff;">J95 GENERIS PRODUCTION</h1>
    <p style="color: #00ffcc; font-family: monospace;">// PORTAL_v17.0</p>
</div>
""", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["[ 01_BOOK_SESSION ]", "[ 02_DEPOSIT_LINK ]", "[ 03_TERMINATE_LINK ]"])

# --- TAB 1: BOOKING SYSTEM ---
with t1:
    st.write("### 🎵 1. UPLOAD REFERENCE")
    ref_song = st.file_uploader("Select MP3/WAV (Max 200MB)", type=['mp3', 'wav', 'm4a'])
    if ref_song:
        st.success(f"FILE_LOADED: {ref_song.name}")
    
    st.write("---")
    st.write("### 📅 2. SESSION DETAILS")
    
    with st.form("booking_form"):
        c1, c2 = st.columns(2)
        with c1:
            nm = st.text_input("👤 ARTIST_ID (NAME)")
        with c2:
            dt = st.date_input("📅 TARGET_DATE", min_value=date.today(), format="DD/MM/YYYY")
            
        c3, c4 = st.columns(2)
        with c3:
            session_options = ["2 Hour Quick Session", "3 Hour Standard Session", "6 Hour Full Day"]
            selected_type = st.
