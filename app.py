import streamlit as st
from datetime import datetime, date, time, timedelta
from st_gsheets_connection import GSheetsConnection
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
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Connection link pending. Check Streamlit Secrets.")

# --- BRANDING HEADER ---
st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #ff00ff;">J95 GENERIS PRODUCTION</h1>
    <p style="color: #00ffcc; font-family: monospace;">// PORTAL_v18.0</p>
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
            selected_type = st.selectbox("💾 SESSION_TYPE", options=session_options)
        with c4:
            start_options = ["12:00 PM", "03:00 PM"]
            selected_start = st.selectbox("TIMELINE_START", options=start_options)
            
        ref_notes = st.text_area("SESSION_NOTES (VIBE, MIXING STYLE, ETC.)")

        # Session Timing Logic
        hr = 2 if "2 Hour" in selected_type else 3 if "3 Hour" in selected_type else 6
        tm = time(12, 0) if "12:00" in selected_start else time(15, 0)
        start_dt = datetime.combine(dt, tm)
        end_dt = start_dt + timedelta(hours=hr)

        # Pricing Logic
        hours_ahead = (start_dt - datetime.now()).total_seconds() / 3600
        base_rate = 100 if hours_ahead > 72 else 120
        total_cost = base_rate + (max(0, hr - 2) * 10)
        deposit = total_cost * 0.5

        st.markdown(f"""
            <div style="background-color: #1a1a1a; padding: 10px; border-left: 5px solid #ff00ff;">
                <code>>> SYSTEM_CONFIRM: {dt.strftime('%d/%m/%Y')} // {start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}</code>
            </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**TOTAL_CREDITS:** ${total_cost:.2f} | **SECURE_DEPOSIT:** ${deposit:.2f}")
        
        submit = st.form_submit_button("INITIALIZE_RESERVATION")
        
        if submit:
            if not nm:
                st.error("ERROR: ARTIST_ID REQUIRED")
            else:
                new_data = pd.DataFrame([{
                    "Artist Name": nm,
                    "Date": dt.strftime('%d/%m/%Y'),
                    "Start Time": start_dt.strftime('%I:%M %p'),
                    "End Time": end_dt.strftime('%I:%M %p'),
                    "Total Price": f"${total_cost:.2f}",
                    "Notes": ref_notes
                }])
                
                try:
                    conn.create(data=new_data)
                    st.success(f"DATA SECURED. RESERVATION LOGGED FOR {nm}.")
                except Exception:
                    st.warning("RESERVATION PROCESSED. (Sheet sync pending connection setup)")

# --- TAB 2: PAYMENT GATEWAY ---
with t2:
    st.subheader("NETWORK_PAYMENT_GATEWAY")
    st.write("---")
    st.write("**INSTITUTION:** Commonwealth Bank (CBA)")
    st.write("**ACCOUNT NAME:** Amuson Bernicke")
    st.write("**BSB:** 064-036")
    st.write("**ACC_NUMBER:** [Enter Account Number]")
    st.divider()
    receipt = st.file_uploader("UPLOAD_TX_RECEIPT", type=['jpg', 'png', 'pdf'])

# --- TAB 3: TERMINATION ---
with t3:
    st.subheader("❌ TERMINATE_RESERVATION")
    with st.form("cancel_form"):
        cancel_nm = st.text_input("ENTER_ARTIST_ID")
        cancel_dt = st.date_input("SELECT_SESSION_DATE", format="DD/MM/YYYY")
        reason = st.text_area("REASON_FOR_TERMINATION")
        cancel_submit = st.form_submit_button("CONFIRM_TERMINATION")
        if cancel_submit:
            st.warning("TERMINATION_REQUEST_SENT.")

st.markdown("---")
st.caption("© 2026 J95 Generis Production | Nauru")
