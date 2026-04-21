import streamlit as st
from datetime import datetime, date, time, timedelta
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Set up page config
st.set_page_config(page_title="J95 GENERIS PRODUCTION", page_icon="🎙️", layout="centered")

# --- CLEAN CYBERPUNK CSS ---
st.markdown("""

""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- BRANDING HEADER ---
st.markdown("""
    

        
J95 GENERIS PRODUCTION

        
// PORTAL_v17.0

    

""", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["[ 01_BOOK_SESSION ]", "[ 02_DEPOSIT_LINK ]", "[ 03_TERMINATE_LINK ]"])

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
            start_options = ["12:00 PM", "3:00 PM"]
            selected_start = st.selectbox("TIMELINE_START", options=start_options)

        ref_notes = st.text_area("SESSION_NOTES (VIBE, MIXING STYLE, ETC.)")

        # Logic for Session Timing
        hr = 2 if "2 Hour" in selected_type else 3 if "3 Hour" in selected_type else 6
        tm = time(12, 0) if "12:00" in selected_start else time(15, 0)
        start = datetime.combine(dt, tm)
        end = start + timedelta(hours=hr)
        
        # PRICING LOGIC: $100 for more than 3 days, $120 for urgent
        hours_ahead = (start - datetime.now()).total_seconds() / 3600
        base_rate = 100 if hours_ahead > 72 else 120

        # Extra hours cost ($10/hr after the first 2 hours)
        total_cost = base_rate + (max(0, hr - 2) * 10)
        deposit = total_cost * 0.5

        st.markdown(f"""
        

            >> SYSTEM_CONFIRM: {dt.strftime('%d/%m/%Y')} // {start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}
        

        """, unsafe_allow_html=True)
        
        st.write(f"**TOTAL_CREDITS:** ${total_cost:.2f} | **SECURE_DEPOSIT:** ${deposit:.2f}")

        submit = st.form_submit_button("INITIALIZE_RESERVATION")
        if submit:
            if not nm:
                st.error("ERROR: ARTIST_ID REQUIRED")
            else:
                # Prepare data for Google Sheets
                new_data = pd.DataFrame([{
                    "Artist Name": nm,
                    "Date": dt.strftime('%d/%m/%Y'),
                    "Start Time": start.strftime('%I:%M %p'),
                    "End Time": end.strftime('%I:%M %p'),
                    "Total Price": f"${total_cost:.2f}",
                    "Notes": ref_notes
                }])
                
                # Append to Google Sheet
                try:
                    conn.create(data=new_data)
                    st.success(f"DATA SECURED. RESERVATION LOGGED FOR {nm}.")
                except Exception as e:
                    st.warning("RESERVATION PROCESSED. (Sheet sync pending connection setup)")

with t2:
    st.subheader("NETWORK_PAYMENT_GATEWAY")
    st.write("---")
    st.write("**INSTITUTION:** Commonwealth Bank")
    st.write("**ID:** Amuson Bernicke")
    st.write("**BSB:** 064-036")
    st.write("**ACC_NUMBER:** XXXX XXXX")
    st.divider()
    receipt = st.file_uploader("UPLOAD_TX_RECEIPT", type=['jpg', 'png', 'pdf'])

with t3:
    st.subheader("❌ TERMINATE_RESERVATION")
    with st.form("cancel_form"):
        cancel_nm = st.text_input("ENTER_ARTIST_ID")
        cancel_dt = st.date_input("SELECT_SESSION_DATE", format="DD/MM/YYYY")
        reason = st.text_area("REASON_FOR_TERMINATION")
        cancel_submit = st.form_submit_button("CONFIRM_TERMINATION")
        if cancel_submit:
            st.warning(f"TERMINATION_REQUEST_SENT: Our system operator will review the cancellation.")
