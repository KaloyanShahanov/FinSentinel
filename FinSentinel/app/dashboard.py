import streamlit as st

def show_alerts(alerts):
    st.title("Alerts Dashboard")
    for alert in alerts:
        st.write(alert)
