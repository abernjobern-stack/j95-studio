mport streamlit as st
from datetime import datetime, date, time, timedelta

# Set up page config
st.set_page_config(page_title="J95 STUDIO // CYBERPUNK", page_icon="🎙️", layout="centered")

# --- CYBERPUNK CSS INJECTION ---
st.markdown("""

""", unsafe_allow_html=True)

st.title("⚡ J95-STUDIO // NEON_PORTAL")
st.write("---")
st.write("SYSTEM_OPERATOR: Amuson Bernicke")

t1, t2 = st.tabs(["[ 01_BOOK_SESSION ]", "[ 02_DEPOSIT_LINK ]"])

with t1:
    with st.form("booking_form"):
        nm = st.text_input("ARTIST_ID (NAME)")
        dt = st.date_input("TARGET_DATE", min_value=date.today(), format="DD/MM/YYYY")

        session_options = [
            "2 Hour Quick Session",
            "3 Hour Standard Session",
            "6 Hour Full Day"
        ]
        selected_type = st.selectbox("SESSION_TYPE", options=session_options)

        start_options = ["12:00 PM", "3:00 PM"]
        selected_start = st.selectbox("TIMELINE_START", options=start_options)

        # Duration Logic
        if "2 Hour" in selected_type:
            hr = 2
        elif "3 Hour" in selected_type:
            hr = 3
        else:
            hr = 6

        # Start Time Logic
        if "12:00" in selected_start:
            tm = time(12, 0)
        else:
            tm = time(15, 0)

        start = datetime.combine(dt, tm)
        end = start + timedelta(hours=hr)
        
        # Pricing Logic (4-day advance discount)
        days_ahead = (start - datetime.now()).days
        hours_ahead = (start - datetime.now()).total_seconds() / 3600
        
        if days_ahead >= 4:
            base_rate = 100
        elif hours_ahead < 72:
            base_rate = 120
        else:
            base_rate = 100

        extra_hours_cost = max(0, hr - 2) * 10
        total_cost = base_rate + extra_hours_cost
        deposit = total_cost * 0.5

        st.info(f"CONFIRMED: {dt.strftime('%d/%m/%Y')} // {start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}")
        
        st.write(f"**TOTAL_CREDITS:** ${total_cost:.2f}")
        st.write(f"**SECURE_DEPOSIT (50%):** ${deposit:.2f}")

        submit = st.form_submit_button("INITIALIZE_RESERVATION")
        if submit:
            st.success(f"DATA_LINK_ESTABLISHED: {nm}. Awaiting verification.")

with t2:
    st.subheader("NETWORK_PAYMENT_GATEWAY")
    st.markdown("""
    Transfer credits to the following terminal:
    
    * **INSTITUTION:** Commonwealth Bank
    * **ID:** Amuson Bernicke
    * **BSB:** 064-036
    * **ACC_NUMBER:** XXXX XXXX
    
    *Physical credit exchange accepted at terminal.*
    """)
    
    st.divider()
    
    st.write("### UPLOAD_TX_RECEIPT")
    receipt = st.file_uploader("Scan and upload receipt (JPG/PNG/PDF)", type=['jpg', 'png', 'pdf'])
    
    if receipt:
        st.success("TRANSMISSION_RECEIVED. Verifying credentials...")
