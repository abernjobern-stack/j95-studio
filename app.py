import streamlit as st
from datetime import datetime, date, time, timedelta

# Set up page config for a professional look
st.set_page_config(page_title="J95 Studio Booking", page_icon="🎙️")

st.title("🎙️ J95-Studio Booking Portal")
st.write("Lead Engineer: Amuson Bernicke")

# Create Tabs for a cleaner mobile UI
t1, t2 = st.tabs(["1. Book Session", "2. Payment & Deposit"])

with t1:
    with st.form("booking_form"):
        nm = st.text_input("Artist Name")
        dt = st.date_input("Date", min_value=date.today())
        tm = st.time_input("Start Time", value=time(14, 0))
        hr = st.number_input("Duration (Hours)", min_value=2, max_value=12, value=2)

        # Logic for Session Timing
        start = datetime.combine(dt, tm)
        end = start + timedelta(hours=hr)
        
        # Logic for Pricing (Urgent = < 72 hours notice)
        urg = (start - datetime.now()).total_seconds() / 3600 < 72
        base_rate = 120 if urg else 100
        extra_hours_cost = max(0, hr - 2) * 10
        total_cost = base_rate + extra_hours_cost
        deposit = total_cost * 0.5

        st.info(f"Booking: {start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')}")
        
        st.write(f"**Total Price:** ${total_cost:.2f}")
        st.write(f"**Required Deposit (50%):** ${deposit:.2f}")

        submit = st.form_submit_button("RESERVE SESSION")
        if submit:
            st.success(f"Request sent for {nm}! Please proceed to the Deposit tab.")

with t2:
    st.subheader("Deposit & Verification")
    st.markdown("""
    To secure your slot, please transfer the 50% deposit to the following account:
    
    * **Bank:** Commonwealth Bank
    * **Acc Name:** Amuson Bernicke
    * **BSB:** 064-036 
    * **Acc #:** 1001 2283
    
    *Note: Cash payments are also accepted in person.*"""
    \"\"\")
    
    st.divider()
    
    st.write("### Upload Receipt")
    receipt = st.file_uploader("Upload a screenshot of your transfer", type=['jpg', 'png', 'pdf'])
    
    if receipt:
        st.success("Receipt uploaded! We will verify and confirm your session shortly.")
