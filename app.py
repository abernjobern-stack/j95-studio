import streamlit as st
from datetime import datetime, date, timedelta, time

st.set_page_config(page_title="J95 Studio", page_icon="🎙️")

st.markdown("""

""", unsafe_allow_html=True)

st.title("🎙️ Generis Production")
st.write("Lead Engineer: **J95**")

t1, t2, t3 = st.tabs(["Booking", "Payment", "Reference"])

with t1:
    st.subheader("1. Schedule")
    with st.form("f1"):
        nm = st.text_input("Artist Name")
        dt = st.date_input("Date", min_value=date.today())
        tm = st.time_input("Start", value=time(14, 0))
        hr = st.number_input("Hours", min_value=2, max_value=12, value=2)
        start = datetime.combine(dt, tm)
        end = start + timedelta(hours=hr)
        urg = (start - datetime.now()).total_seconds() / 3600 < 72
        cost = (120 if urg else 100) + (max(0, hr - 2) * 10)
        st.markdown(f"

{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}
", unsafe_allow_html=True)
        st.markdown(f"

Deposit: ${cost * 0.5}
Total: ${cost}
", unsafe_allow_html=True)
        st.form_submit_button("SUBMIT")

with t2:
    st.subheader("2. Deposit")
    st.markdown("
Acc: Amuson Bernicke
BSB: 064-036
Acc #: 1001 2283
", unsafe_allow_html=True)
    st.file_uploader("Upload Receipt", type=['jpg', 'png'])
    st.button("Send Receipt")

with t3:
    st.subheader("3. Music")
    st.file_uploader("Upload MP3/WAV", type=['mp3', 'wav'])
    st.button("Send to J95")
