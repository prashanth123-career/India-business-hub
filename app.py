# requirements.txt
streamlit==1.33.0
streamlit-chat==0.1.0
pandas==2.0.3
python-dotenv==1.0.0
pywhatkit==5.4

# app.py
import streamlit as st
from streamlit_chat import message
import pandas as pd
from dotenv import load_dotenv
import pywhatkit as pwk
import time
import os

load_dotenv()

# WhatsApp numbers
INDIA_WHATSAPP = "+917975931377"
UK_WHATSAPP = "+447712463573"

def initialize_session():
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = {
            'name': '',
            'email': '',
            'phone': '',
            'business_type': '',
            'direction': '',
            'requirements': []
        }
    if 'stage' not in st.session_state:
        st.session_state['stage'] = 'welcome'

def get_business_advice(direction, business_type):
    """Provide basic advice based on user inputs"""
    advice = {
        ('India to UK', 'Manufacturing'): [
            "1. Register as a UK Limited Company",
            "2. Obtain UKCA certification for products",
            "3. Setup VAT registration",
            f"Contact UK expert: {UK_WHATSAPP}"
        ],
        ('UK to India', 'Services'): [
            "1. Choose between Liaison Office/Branch/Subsidiary",
            "2. Register with RBI under FEMA",
            "3. GST registration required",
            f"Contact India expert: {INDIA_WHATSAPP}"
        ]
    }
    return advice.get((direction, business_type), [
        "General advice:",
        "1. Conduct market research",
        "2. Choose appropriate business structure",
        "3. Ensure tax compliance",
        f"Contact experts: India {INDIA_WHATSAPP} | UK {UK_WHATSAPP}"
    ])

def collect_user_info():
    """Multi-stage form to collect user requirements"""
    stages = {
        'welcome': {
            'question': "Welcome to Indo-UK Business Assistant! Shall we begin? (Yes/No)",
            'handler': lambda x: 'name' if x.lower() == 'yes' else 'exit'
        },
        'name': {
            'question': "Please enter your full name:",
            'handler': lambda x: 'email'
        },
        'email': {
            'question': "Please enter your email address:",
            'handler': lambda x: 'phone'
        },
        'phone': {
            'question': "Please enter your phone number with country code:",
            'handler': lambda x: 'direction'
        },
        'direction': {
            'question': "What type of business setup are you looking for? (India to UK / UK to India)",
            'handler': lambda x: 'business_type'
        },
        'business_type': {
            'question': "What is your business type? (Manufacturing/Services/Trading/Other)",
            'handler': lambda x: 'requirements'
        },
        'requirements': {
            'question': "Please describe your specific requirements (type 'done' when finished):",
            'handler': lambda x: 'summary' if x.lower() == 'done' else 'requirements'
        }
    }
    
    current_stage = st.session_state['stage']
    stage_config = stages[current_stage]
    
    return stage_config['question'], stage_config['handler']

def send_whatsapp_message(number, message):
    """Send message via WhatsApp (requires web.whatsapp.com open in browser)"""
    try:
        pwk.sendwhatmsg_instantly(
            phone_no=number,
            message=message,
            wait_time=15,
            tab_close=True
        )
        return True
    except Exception as e:
        st.error(f"Couldn't send WhatsApp message: {str(e)}")
        return False

def main():
    st.title("Indo-UK Business Setup Assistant 💼🌐")
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
    
    initialize_session()
    
    # Chat interface
    response_container = st.container()
    input_container = st.container()
    
    with input_container:
        user_input = st.chat_input("Type your message here...", key="input")
        
        if user_input:
            st.session_state['past'].append(user_input)
            
            if st.session_state['stage'] == 'exit':
                st.session_state['generated'].append("Thank you for using our service. Have a great day!")
            else:
                question, handler = collect_user_info()
                
                # Handle different stages
                if st.session_state['stage'] == 'name':
                    st.session_state['user_data']['name'] = user_input
                elif st.session_state['stage'] == 'email':
                    st.session_state['user_data']['email'] = user_input
                elif st.session_state['stage'] == 'phone':
                    st.session_state['user_data']['phone'] = user_input
                elif st.session_state['stage'] == 'direction':
                    st.session_state['user_data']['direction'] = user_input
                elif st.session_state['stage'] == 'business_type':
                    st.session_state['user_data']['business_type'] = user_input
                elif st.session_state['stage'] == 'requirements' and user_input.lower() != 'done':
                    st.session_state['user_data']['requirements'].append(user_input)
                
                next_stage = handler(user_input)
                st.session_state['stage'] = next_stage
                
                if next_stage == 'summary':
                    # Prepare summary
                    user_data = st.session_state['user_data']
                    summary = [
                        "Thank you for your information! Here's your summary:",
                        f"Name: {user_data['name']}",
                        f"Business Direction: {user_data['direction']}",
                        f"Business Type: {user_data['business_type']}",
                        "Requirements:",
                        *[f"- {req}" for req in user_data['requirements']],
                        "",
                        "Based on your inputs:"
                    ]
                    
                    # Get business advice
                    advice = get_business_advice(
                        user_data['direction'],
                        user_data['business_type']
                    )
                    
                    # Prepare WhatsApp message
                    whatsapp_msg = (
                        f"New Business Inquiry from {user_data['name']}\n"
                        f"Phone: {user_data['phone']}\n"
                        f"Direction: {user_data['direction']}\n"
                        f"Type: {user_data['business_type']}\n"
                        "Requirements:\n" + 
                        "\n".join(user_data['requirements'])
                    )
                    
                    # Determine which WhatsApp number to use
                    whatsapp_number = UK_WHATSAPP if "UK to India" in user_data['direction'] else INDIA_WHATSAPP
                    
                    # Add WhatsApp contact instructions
                    summary.extend([
                        "",
                        "For detailed consultation:",
                        f"Contact our {'UK' if 'UK to India' in user_data['direction'] else 'India'} expert on WhatsApp:",
                        f"👉 {whatsapp_number}",
                        "",
                        "Click below to start WhatsApp chat:",
                    ])
                    
                    st.session_state['generated'].append("\n".join(summary))
                    st.session_state['generated'].append(advice)
                    
                    # Attempt to send WhatsApp message
                    if send_whatsapp_message(whatsapp_number, whatsapp_msg):
                        st.session_state['generated'].append("(We've notified our expert about your inquiry)")
                else:
                    next_question, _ = collect_user_info()
                    st.session_state['generated'].append(next_question)
    
    # Display chat history
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                if i < len(st.session_state['past']):
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                
                # Render WhatsApp button for contact info
                if any(num in str(st.session_state['generated'][i]) for num in [INDIA_WHATSAPP, UK_WHATSAPP]):
                    msg = st.session_state['generated'][i]
                    st.markdown(msg)
                    
                    # Determine which number to use
                    whatsapp_num = UK_WHATSAPP if UK_WHATSAPP in msg else INDIA_WHATSAPP
                    country = "UK" if whatsapp_num == UK_WHATSAPP else "India"
                    
                    whatsapp_url = f"https://wa.me/{whatsapp_num.replace('+', '')}"
                    st.markdown(
                        f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">'
                        f'Chat with {country} Expert</a>',
                        unsafe_allow_html=True
                    )
                else:
                    message(st.session_state['generated'][i], key=str(i))
    
    # Sidebar with quick contact options
    st.sidebar.header("Quick Connect")
    st.sidebar.markdown(f"""
    **India Expert:**
    [WhatsApp {INDIA_WHATSAPP}](https://wa.me/{INDIA_WHATSAPP.replace('+', '')})
    
    **UK Expert:**
    [WhatsApp {UK_WHATSAPP}](https://wa.me/{UK_WHATSAPP.replace('+', '')})
    """)
    
    st.sidebar.header("Common Queries")
    if st.sidebar.button("Manufacturing Setup"):
        st.session_state['past'].append("Manufacturing Setup")
        st.session_state['generated'].append(get_business_advice("India to UK", "Manufacturing"))
    
    if st.sidebar.button("Service Business"):
        st.session_state['past'].append("Service Business")
        st.session_state['generated'].append(get_business_advice("UK to India", "Services"))

if __name__ == "__main__":
    main()
