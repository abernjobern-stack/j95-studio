import streamlit as st
from datetime import datetime, date, time, timedelta

# Set up page config
st.set_page_config(page_title="J95 GENERIS PRODUCTION", page_icon="🎙️", layout="centered")

# --- CLEAN CYBERPUNK CSS ---
st.markdown("""

""", unsafe_allow_html=True)

# --- BRANDING HEADER ---
st.markdown("""
    

        
J95 GENERIS PRODUCTION

        
// PORTAL_v14.0

    

""", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["[ 01_BOOK_SESSION ]", "[ 02_DEPOSIT_LINK ]", "[ 03_TERMINATE_LINK ]"])

with t1:
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

        st.write("---")
        st.write("### 🎵 REFERENCE_MATERIAL")
        ref_song = st.file_uploader("UPLOAD_REFERENCE_TRACK (MP3, WAV, M4A)", type=['mp3', 'wav', 'm4a'])
        ref_notes = st.text_area("SESSION_NOTES (E.G. VIBE, MIXING STYLE)")

        # Duration Logic
        hr = 2 if "2 Hour" in selected_type else 3 if "3 Hour" in selected_type else 6
        tm = time(12, 0) if "12:00" in selected_start else time(15, 0)

        start = datetime.combine(dt, tm)
        end = start + timedelta(hours=hr)
        
        # Pricing Logic
        days_ahead = (start - datetime.now()).days
        hours_ahead = (start - datetime.now()).total_seconds() / 3600
        base_rate = 100 if (days_ahead >= 4 or hours_ahead >= 72) else 120
        total_cost = base_rate + (max(0, hr - 2) * 10)
        deposit = total_cost * 0.5

        st.markdown(f"""
        

            >> SYSTEM_CONFIRM: {dt.strftime('%d/%m/%Y')} // {start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}
        

        """, unsafe_allow_html=True)
        
        st.write(f"**TOTAL_CREDITS:** ${total_cost:.2f} | **SECURE_DEPOSIT:** ${deposit:.2f}")

        submit = st.form_submit_button("INITIALIZE_RESERVATION")
        if submit:
            st.success(f"DATA_LINK_ESTABLISHED: {nm}. Reference received. Proceed to Deposit.")

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
