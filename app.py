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

        # Define 2 Sessions per day
        session_options = [
            "Afternoon Session (12:00 PM - 3:00 PM)", 
            "Evening Session (3:00 PM - 6:00 PM)"
        ]

        selected_session = st.selectbox("Select Session Slot", options=session_options)

        # Logic for Session Times and Duration (Both are 3 hours)
        hr = 3
        if "Afternoon" in selected_session:
            tm = time(12, 0)
        else:
            tm = time(15, 0)

        # Logic for Session Timing calculation
        start = datetime.combine(dt, tm)
        end = start + timedelta(hours=hr)
        
        # Pricing Logic
        days_ahead = (start - datetime.now()).days
        hours_ahead = (start - datetime.now()).total_seconds() / 3600
        
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

        # Displaying the formatted date to the user
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
    * **Acc #:** XXXX XXXX
    
    *Note: Cash payments are also accepted in person.*
    """)
    
    st.divider()
    
    st.write("### Upload Receipt")
    receipt = st.file_uploader("Upload a screenshot of your transfer", type=['jpg', 'png', 'pdf'])
    
    if receipt:
        st.success("Receipt uploaded! We will verify and confirm your session shortly.")
