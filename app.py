import streamlit as st
from datetime import datetime, date, time, timedelta

# Set up page config
st.set_page_config(page_title="J95 Studio Booking", page_icon="🎙️")

st.title("🎙️ J95-Studio Booking Portal")
st.write("Lead Engineer: Amuson Bernicke")

t1, t2 = st.tabs(["1. Book Session", "2. Payment & Deposit"])

with t1:
    with st.form("booking_form"):
        nm = st.text_input("Artist Name")
        
        # Calendar booking in Day/Month/Year format
        dt = st.date_input("Date", min_value=date.today(), format="DD/MM/YYYY")

        # You choose the session lengths available to them
        session_options = [
            "2 Hour Quick Session",
            "3 Hour Standard Session",
            "6 Hour Full Day"
        ]
        
        selected_type = st.selectbox("Select Session Type", options=session_options)

        # Start Time Selection
        start_options = ["12:00 PM", "3:00 PM"]
        selected_start = st.selectbox("Select Start Time", options=start_options)

        # Set duration (hr) based on your chosen session types
        if "2 Hour" in selected_type:
            hr = 2
        elif "3 Hour" in selected_type:
            hr = 3
        else:
            hr = 6

        # Convert start time selection to time object
        if "12:00" in selected_start:
            tm = time(12, 0)
        else:
            tm = time(15, 0)

        # Logic for Session Timing calculation
        start = datetime.combine(dt, tm)
        end = start + timedelta(hours=hr)
        
        # Pricing Logic
        days_ahead = (start - datetime.now()).days
        hours_ahead = (start - datetime.now()).total_seconds() / 3600
        
        # Base rate: $100 unless it is urgent (less than 72 hours and not 4+ days ahead)
        if days_ahead >= 4:
            base_rate = 100
        elif hours_ahead < 72:
            base_rate = 120
        else:
            base_rate = 100

        # Extra hours cost ($10/hr after the first 2 hours)
        extra_hours_cost = max(0, hr - 2) * 10
        total_cost = base_rate + extra_hours_cost
        deposit = total_cost * 0.5

        # Displaying the formatted date and session info
        st.info(f"Booking for {dt.strftime('%d/%m/%Y')}: {start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')}")
        
        st.write(f"**Total Price:** ${total_cost:.2f}")
        st.write(f"**Required Deposit (50%):** ${deposit:.2f}")

        submit = st.form_submit_button("RESERVE SESSION")
        if submit:
            st.success(f"Request sent for {nm}! Please proceed to the Deposit tab.")

with t2:
    st.subheader("2. Deposit & Verification")
    st.markdown("""
    To secure your slot, please transfer the 50% deposit to the following account:
    
    * **Bank:** Commonwealth Bank
    * **Acc Name:** Amuson Bernicke
    * **BSB:** 064-036
    * **Acc #:** 1001 2283
    
    *Note: Cash payments are also accepted in person.*
    """)
    
    st.divider()
    
    st.write("### Upload Receipt")
    receipt = st.file_uploader("Upload a screenshot of your transfer", type=['jpg', 'png', 'pdf'])
    
    if receipt:
        st.success("Receipt uploaded! We will verify and confirm your session shortly.")
