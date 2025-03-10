import streamlit as st
from forex_python.converter import CurrencyRates
from dotenv import load_dotenv
import os
import requests


# Load environment variables
load_dotenv("api_key.env")

# Function to get AI response from Hugging Face
def get_free_ai_response(prompt):
    print(f"Prompt received: {prompt}")  # Debugging print statement

    # ✅ Use a correct Hugging Face model
    url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
    data = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=data)
    print(f"API Response Status: {response.status_code}")  # Debugging print statement

    if response.ok:
        try:
            ai_response = response.json()[0].get("generated_text", "No response from AI")
            print(f"AI Response: {ai_response}")  # Debugging print statement
            return ai_response
        except (KeyError, IndexError):
            return "Error: Unexpected response format."
    else:
        return f"Error: {response.text}"  # Return the actual API error message

# Set Background Style
st.markdown(
    """
    <style>
    .stApp {
        background: url('https://wallscloud.net/img/resize/1600/900/MM/2017-02-11-wallpaper_by_cybacreep-d7hprs3.jpg') no-repeat center center fixed;
        background-size: cover;
    }
        </style>
    """,
    unsafe_allow_html=True
)

# Function to handle unit conversion
def convert_units(value, from_unit, to_unit, category):
    conversion_factors = {
        "Length": {"meter": 1, "kilometer": 0.001, "mile": 0.000621371, "foot": 3.28084},
        "Weight": {"gram": 1, "kilogram": 0.001, "pound": 0.00220462, "ounce": 0.035274},
        "Temperature": {"Celsius": "C", "Fahrenheit": "F", "Kelvin": "K"},
    }
    
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
        else:
            return value
    
    elif category in conversion_factors:
        return value * conversion_factors[category][to_unit] / conversion_factors[category][from_unit]
    
    return None

# Streamlit UI
st.markdown("<h1 class='stTitle'>UnitSense AI</h1>", unsafe_allow_html=True)

categories = ["Length", "Weight", "Temperature"]
selected_category = st.selectbox("Select Category", categories)

units = {
    "Length": ["meter", "kilometer", "mile", "foot"],
    "Weight": ["gram", "kilogram", "pound", "ounce"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
}

from_unit = st.selectbox("From Unit", units[selected_category])
to_unit = st.selectbox("To Unit", units[selected_category])
value = st.number_input("Enter Value", min_value=0.0, format="%.2f")

if st.button("Convert"):
    result = convert_units(value, from_unit, to_unit, selected_category)
    st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")
    
# Initialize session state for search history
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# AI Chatbot Feature with History
st.markdown("## Ask AI a Question")
prompt = st.text_input("Enter your question:")

if st.button("Ask AI"):
    if prompt:
        response = get_free_ai_response(prompt)
        st.session_state.search_history.append((prompt, response))  # Store question and response
        st.write(response)
    else:
        st.warning("Please enter a question.")

# Display AI Search History
if st.session_state.search_history:
    st.markdown("### Search History")
    for i, (question, answer) in enumerate(reversed(st.session_state.search_history), 1):
        with st.expander(f"Question {i}: {question}"):
            st.write(answer)
