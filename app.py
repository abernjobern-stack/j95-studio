import streamlit as st
from datetime import datetime, date, timedelta, time

st.set_page_config(page_title="Generis Production | J95", page_icon="🎙️")

# --- DARK THEME UI ---
st.markdown("""

""", unsafe_allow_html=True)

st.title("🎙️ Generis Production")
st.write("Lead Engineer: **J95**")

tab1, tab2, tab3 = st.tabs(["📅 1. Book Session", "📑 2. Proof of Payment", "🎵 3. Song Reference"])

# --- TAB 1: BOOKING ---
with tab1:
    st.subheader("Step 1: Schedule Your Time")
    with st.form("booking_form"):
        artist_name = st.text_input("Artist Name")
        col1, col2 = st.columns(2)
        with col1:
            booking_date = st.date_input("Date", min_value=date.today())
            start_time = st.time_input("Start Time", value=time(14, 0))
        with col2:
            duration = st.number_input("Total Hours", min_value=2, max_value=12, value=2)

        # PRICING LOGIC
        start_dt = datetime.combine(booking_date, start_time)
        end_dt = start_dt + timedelta(hours=duration)
        is_urgent = (start_dt - datetime.now()).total_seconds() / 3600 < 72
        base_price = 120 if is_urgent else 100
        total_cost = base_price + (max(0, duration - 2) * 10)
        deposit_amount = total_cost * 0.50

        st.markdown(f"

Window: {start_dt.strftime('%I:%M %p')} — {end_dt.strftime('%I:%M %p')}
", unsafe_allow_html=True)
        st.markdown(f"

Total: ${total_cost}
Deposit Required: ${deposit_amount}
", unsafe_allow_html=True)
        
        if st.form_submit_button("SUBMIT REQUEST"):
            st.success("Request Submitted! Now proceed to Step 2.")

# --- TAB 2: PROOF OF PAYMENT ---
with tab2:
    st.subheader("Step 2: Verify Your Deposit")
    st.markdown(f"

Bank Transfer Details:
Acc Name: Amuson Bernicke
BSB: 064-036
Acc #: 1001 2283
", unsafe_allow_html=True)
    
    pay_artist = st.text_input("Confirm Artist Name for Payment")
    receipt_file = st.file_uploader("Upload Receipt Screenshot", type=['jpg', 'png'])
    
    if st.button("Submit Proof of Payment"):
        if receipt_file and pay_artist:
            st.success("Receipt uploaded! J95 will verify shortly.")
        else:
            st.error("Please upload a receipt and enter your name.")

# --- TAB 3: SONG REFERENCE ---
with tab3:
    st.subheader("Step 3: Prepare the Session")
    artist_ref = st.text_input("Artist Name (Reference)")
    song_file = st.file_uploader("Upload MP3/WAV", type=['mp3', 'wav'])
    if st.button("Send Track to Studio"):
        st.success("File received! J95 is getting the session ready.")
