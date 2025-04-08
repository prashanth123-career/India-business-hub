# app.py
import streamlit as st
import pandas as pd

# --- WhatsApp numbers ---
INDIA_WHATSAPP = "+917975931377"
UK_WHATSAPP = "+447712463573"

# --- Business Setup Options ---
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

def inject_custom_css():
    st.markdown("""
        <style>
        /* Hide default Streamlit UI */
        #MainMenu, footer, header {visibility: hidden;}
        
        /* Style for WhatsApp Button */
        .whatsapp-btn {
            background-color: #25D366;
            color: white;
            padding: 10px 18px;
            font-size: 16px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
        }
        .whatsapp-btn:hover {
            background-color: #1DA851;
            color: white;
        }

        .stRadio > div {
            padding-bottom: 10px;
        }

        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            padding: 10px 18px;
            border-radius: 8px;
        }

        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="🌍 Global Business Setup Advisor", layout="wide")  # ✅ MUST be first Streamlit call
    inject_custom_css()  # ✅ Custom styles
    st.title("🌐 Global Business Setup Advisor")
    st.markdown("Your expert guide to setting up your business in **India**, **UK**, or **Cross-Border**.")

    # Session state initialization
    if 'stage' not in st.session_state:
        st.session_state.stage = "selection"
        st.session_state.user_choices = {}

    # Step 1: Choose setup location
    if st.session_state.stage == "selection":
        st.subheader("📍 Where do you want to set up your business?")
        option = st.radio("", list(BUSINESS_OPTIONS.keys()))
        if st.button("Next ➡️"):
            st.session_state.user_choices["business_type"] = option
            st.session_state.stage = "subtype"

    # Step 2: Choose structure
    elif st.session_state.stage == "subtype":
        business_type = st.session_state.user_choices["business_type"]
        subtypes = BUSINESS_OPTIONS[business_type]["types"]

        st.subheader(f"🏢 Select your {business_type} structure:")
        subtype = st.radio("Choose one:", subtypes)
        if st.button("Next ➡️"):
            st.session_state.user_choices["subtype"] = subtype
            st.session_state.stage = "features"
        if st.button("⬅️ Back"):
            st.session_state.stage = "selection"

    # Step 3: Show details
    elif st.session_state.stage == "features":
        business_type = st.session_state.user_choices["business_type"]
        subtype = st.session_state.user_choices["subtype"]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"🔎 Features of **{subtype}**:")
            for f in BUSINESS_OPTIONS[business_type]["features"].get(subtype, ["Details coming soon."]):
                st.markdown(f)
            st.markdown("---")
            st.subheader("📈 Market Benefits")
            if "India" in business_type:
                st.markdown("🇮🇳 **India**")
                st.markdown("- Fast-growing economy (7%+ GDP growth)")
                st.markdown("- Startup India support schemes")
                st.markdown("- Lower cost of operations")
            elif "UK" in business_type:
                st.markdown("🇬🇧 **UK**")
                st.markdown("- 8th globally in ease of business")
                st.markdown("- Stable regulations & IP laws")
                st.markdown("- Strong financial ecosystem")

        with col2:
            st.subheader("📜 Legal Requirements")
            for req in BUSINESS_OPTIONS[business_type]["legal"]:
                st.markdown(req)

            st.markdown("---")
            st.subheader("🛠️ Our Support Includes")
            st.markdown("✅ Company registration & filing")
            st.markdown("✅ Tax, GST/VAT, compliance")
            st.markdown("✅ Bank account opening")
            st.markdown("✅ Ongoing business advisory")

            # WhatsApp CTA
            whatsapp_number = UK_WHATSAPP if "UK" in business_type else INDIA_WHATSAPP
            country = "UK" if "UK" in business_type else "India"
            message = (f"Hello! I need help setting up {subtype} "
                      f"for {business_type}. Please contact me.")
            st.markdown("### 📞 Get Expert Assistance")
            st.markdown(
                f'<a href="{get_whatsapp_link(whatsapp_number, message)}" '
                f'class="whatsapp-btn" target="_blank">'
                f'💬 Chat with {country} Business Expert</a>',
                unsafe_allow_html=True
            )

        st.markdown("---")
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("⬅️ Back"):
                st.session_state.stage = "subtype"
        with col2:
            if st.button("🔄 Restart"):
                st.session_state.stage = "selection"
                st.session_state.user_choices = {}

if __name__ == "__main__":
    main()
