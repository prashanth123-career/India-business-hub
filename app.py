# app.py
import streamlit as st
import pandas as pd

# WhatsApp numbers
INDIA_WHATSAPP = "+917975931377"
UK_WHATSAPP = "+447712463573"

# Business Setup Options
BUSINESS_OPTIONS = {
    "Setup in India": {
        "types": [
            "Private Limited Company",
            "LLP (Limited Liability Partnership)",
            "One Person Company",
            "Proprietorship"
        ],
        "features": {
            "Private Limited Company": [
                "✅ Limited liability protection",
                "✅ Minimum 2 directors required",
                "✅ 15-30% corporate tax",
                "💼 Ideal for startups seeking investment"
            ],
            "LLP (Limited Liability Partnership)": [
                "✅ Hybrid of company and partnership",
                "✅ No minimum capital requirement",
                "✅ 30% tax on profits",
                "💼 Best for professional services firms"
            ]
        },
        "legal": [
            "📝 Company registration with MCA",
            "📝 GST registration",
            "📝 Professional tax compliance",
            "📝 ESI/PF for employees"
        ]
    },
    "Setup in UK": {
        "types": [
            "Limited Company",
            "Partnership",
            "Sole Trader",
            "PLC (Public Limited Company)"
        ],
        "features": {
            "Limited Company": [
                "✅ Separate legal entity",
                "✅ £12,500 tax-free personal allowance",
                "✅ 19-25% corporation tax",
                "💼 Most popular for small businesses"
            ],
            "Sole Trader": [
                "✅ Simplest business structure",
                "✅ Complete control",
                "✅ Personal liability",
                "💼 Ideal for freelancers"
            ]
        },
        "legal": [
            "📝 Companies House registration",
            "📝 VAT registration if turnover >£85k",
            "📝 PAYE for employees",
            "📝 Annual accounts filing"
        ]
    },
    "India-UK Cross Border": {
        "types": [
            "UK Subsidiary of Indian Company",
            "India Branch Office of UK Company",
            "Joint Venture",
            "Representative Office"
        ],
        "features": {
            "UK Subsidiary of Indian Company": [
                "✅ Separate legal entity in UK",
                "✅ Easier access to EU markets",
                "✅ RBI approval required",
                "💼 Best for established Indian companies"
            ],
            "India Branch Office of UK Company": [
                "✅ Can repatriate profits to UK",
                "✅ Restricted activities",
                "✅ RBI/FEMA compliance",
                "💼 For UK companies wanting Indian presence"
            ]
        },
        "legal": [
            "📝 RBI approval for Indian entity",
            "📝 FEMA compliance",
            "📝 Double taxation avoidance",
            "📝 Transfer pricing documentation"
        ]
    }
}

def get_whatsapp_link(number, message):
    return f"https://wa.me/{number.strip('+')}?text={message}"

def main():
    st.set_page_config(page_title="Global Business Setup Advisor", layout="wide")
    st.title("🌐 Global Business Setup Advisor")
    
    # Initialize session state
    if 'stage' not in st.session_state:
        st.session_state.stage = "selection"
        st.session_state.user_choices = {}
    
    # Step 1: Business Type Selection
    if st.session_state.stage == "selection":
        st.subheader("What type of business setup do you need?")
        option = st.radio("", list(BUSINESS_OPTIONS.keys()))
        
        if st.button("Next"):
            st.session_state.user_choices["business_type"] = option
            st.session_state.stage = "subtype"
    
    # Step 2: Business Subtype Selection
    elif st.session_state.stage == "subtype":
        business_type = st.session_state.user_choices["business_type"]
        subtypes = BUSINESS_OPTIONS[business_type]["types"]
        
        st.subheader(f"Available {business_type} options:")
        subtype = st.radio("Select your business structure:", subtypes)
        
        if st.button("Next"):
            st.session_state.user_choices["subtype"] = subtype
            st.session_state.stage = "features"
    
    # Step 3: Show Features and Legal Requirements
    elif st.session_state.stage == "features":
        business_type = st.session_state.user_choices["business_type"]
        subtype = st.session_state.user_choices["subtype"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Features of {subtype}:")
            for feature in BUSINESS_OPTIONS[business_type]["features"][subtype]:
                st.markdown(feature)
            
            st.markdown("---")
            st.subheader("Current Market Advantages:")
            if "India" in business_type:
                st.markdown("🇮🇳 **India Benefits:**")
                st.markdown("- Fastest growing major economy (7%+ GDP growth)")
                st.markdown("- PLI schemes for manufacturers")
            elif "UK" in business_type:
                st.markdown("🇬🇧 **UK Benefits:**")
                st.markdown("- Ease of Doing Business Rank: 8th globally")
                st.markdown("- Strong intellectual property protections")
        
        with col2:
            st.subheader("Legal Requirements:")
            for req in BUSINESS_OPTIONS[business_type]["legal"]:
                st.markdown(req)
            
            st.markdown("---")
            st.subheader("Our Services Include:")
            st.markdown("🔹 Complete registration support")
            st.markdown("🔹 Tax compliance guidance")
            st.markdown("🔹 Bank account opening assistance")
            st.markdown("🔹 Ongoing compliance management")
            
            # WhatsApp CTA
            whatsapp_number = UK_WHATSAPP if "UK" in business_type else INDIA_WHATSAPP
            country = "UK" if "UK" in business_type else "India"
            message = (f"Hello! I need help setting up {subtype} "
                      f"for {business_type}. Please contact me.")
            
            st.markdown(f"### Get Expert Assistance")
            st.markdown(
                f'<a href="{get_whatsapp_link(whatsapp_number, message)}" '
                f'class="whatsapp-btn" target="_blank">'
                f'💬 Chat with {country} Business Expert</a>',
                unsafe_allow_html=True
            )
        
        if st.button("Back"):
            st.session_state.stage = "subtype"

if __name__ == "__main__":
    main()
