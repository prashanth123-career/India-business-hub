# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# WhatsApp numbers
INDIA_WHATSAPP = "+917975931377"
UK_WHATSAPP = "+447712463573"

# Current market situation (update these periodically)
MARKET_INSIGHTS = {
    "India to UK": {
        "benefits": [
            "Strong GBP/INR exchange rate favorable for exports",
            "UK-India FTA negotiations progressing well",
            "Growing demand for Indian tech services in UK"
        ],
        "offerings": [
            "UK company registration",
            "VAT compliance",
            "Market entry strategy"
        ]
    },
    "UK to India": {
        "benefits": [
            "India's fast-growing consumer market",
            "Lower operational costs compared to UK",
            "Government incentives for foreign investors"
        ],
        "offerings": [
            "India entity setup (Liaison/Branch/Subsidiary)",
            "GST and tax compliance",
            "Local partnership matching"
        ]
    }
}

def get_whatsapp_link(number, text):
    return f"https://wa.me/{number.strip('+')}?text={text}"

def main():
    st.title("🌍 Indo-UK Business Gateway")
    st.markdown("""
    <style>
    .whatsapp-btn {
        background-color: #25D366;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        text-decoration: none;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'stage' not in st.session_state:
        st.session_state.stage = "direction"
        st.session_state.user_data = {}

    # Step 1: Business Direction
    if st.session_state.stage == "direction":
        st.subheader("Which business direction are you interested in?")
        direction = st.radio("", ["India to UK", "UK to India"])
        
        if st.button("Next"):
            st.session_state.user_data["direction"] = direction
            st.session_state.stage = "offerings"

    # Step 2: Show Offerings and Benefits
    elif st.session_state.stage == "offerings":
        direction = st.session_state.user_data["direction"]
        
        st.subheader(f"Why {direction} is advantageous now:")
        for benefit in MARKET_INSIGHTS[direction]["benefits"]:
            st.markdown(f"✅ {benefit}")
        
        st.subheader("Our specialized services:")
        for service in MARKET_INSIGHTS[direction]["offerings"]:
            st.markdown(f"⭐ {service}")
        
        st.subheader("Get personalized assistance:")
        whatsapp_number = UK_WHATSAPP if direction == "India to UK" else INDIA_WHATSAPP
        country = "UK" if direction == "India to UK" else "India"
        
        # Pre-filled WhatsApp message
        message = (f"Hello! I'm interested in {direction} business setup. "
                  f"Please contact me regarding {MARKET_INSIGHTS[direction]['offerings'][0]}.")
        
        whatsapp_url = get_whatsapp_link(whatsapp_number, message)
        
        st.markdown(
            f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">'
            f'Chat with {country} Expert</a>',
            unsafe_allow_html=True
        )
        
        if st.button("Back"):
            st.session_state.stage = "direction"

if __name__ == "__main__":
    main()
