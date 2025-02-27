import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

conversions = {
    "Length": {"Metre": 1, "Centimetre": 100, "Kilometre": 0.001, "Mile": 0.000621371, "Yard": 1.09361, "Foot": 3.28084, "Inch": 39.3701},
    "Weight": {"Kilogram": 1, "Gram": 1000, "Pound": 2.205},
    "Temperature": {"Celsius": celsius_to_fahrenheit, "Fahrenheit": fahrenheit_to_celsius},
    "Speed": {"Metre per second": 1, "Kilometre per hour": 3.6, "Mile per hour": 2.237},
    "Time": {"Second": 1, "Minute": 1/60, "Hour": 1/3600}
}

unit_details = {
    "Metre": "The basic unit of length in the metric system.",
    "Centimetre": "A unit of length equal to one hundredth of a metre.",
    "Kilometre": "A unit of length equal to 1,000 metres.",
    "Mile": "A unit of length commonly used in the US, equal to 1.609 km.",
    "Yard": "A unit of length equal to 3 feet or 0.9144 metres.",
    "Foot": "A unit of length equal to 12 inches or 0.3048 metres.",
    "Inch": "A unit of length equal to 1/12 of a foot.",
    "Kilogram": "The base unit of mass in the metric system.",
    "Gram": "A unit of mass equal to one thousandth of a kilogram.",
    "Pound": "A unit of weight commonly used in the US and UK, equal to 0.453 kg.",
    "Celsius": "A scale of temperature where water freezes at 0°C and boils at 100°C.",
    "Fahrenheit": "A scale of temperature where water freezes at 32°F and boils at 212°F.",
    "Metre per second": "A unit of speed indicating metres traveled per second.",
    "Kilometre per hour": "A unit of speed commonly used in transportation.",
    "Mile per hour": "A unit of speed used primarily in the US and UK.",
    "Second": "The base unit of time in the SI system.",
    "Minute": "A unit of time equal to 60 seconds.",
    "Hour": "A unit of time equal to 60 minutes."
}

conversion_history = []

def convert_units(category, from_unit, to_unit, value):
    if category == "Temperature":
        return conversions[category][to_unit](value)
    else:
        return value * (conversions[category][to_unit] / conversions[category][from_unit])

st.set_page_config(page_title="Unit Converter", layout="wide")

with st.sidebar:
    st.title("⚙️ Settings")
    user_name = st.text_input("Enter your name")
    if user_name:
        st.write(f"👤 Hello, {user_name}!")
    st.markdown("---")
    st.write("Developed by Sadia")

st.title("🔄 Unit Converter")

category = st.selectbox("Select Category", list(conversions.keys()))
units = {key: list(value.keys()) for key, value in conversions.items()}

from_unit = st.selectbox("From", units[category])
value = st.number_input("Value", min_value=0.0, format="%.2f")
to_unit = st.selectbox("To", units[category])

if st.button("Convert"):
    with st.spinner("Converting..."):
        time.sleep(1)  # Smooth animation effect
    result = convert_units(category, from_unit, to_unit, value)
    st.success(f"✅ {value} {from_unit} = {result:.2f} {to_unit}")
    
    # Show unit details
    st.info(f"ℹ️ {from_unit}: {unit_details.get(from_unit, 'No details available.')}")
    st.info(f"ℹ️ {to_unit}: {unit_details.get(to_unit, 'No details available.')}")
    
    # Store conversion history
    conversion_history.append((value, from_unit, to_unit, result))

# Display conversion history
if conversion_history:
    st.subheader("📜 Conversion History")
    df = pd.DataFrame(conversion_history, columns=["Value", "From", "To", "Result"])
    st.dataframe(df)
    
    if st.button("Clear History"):
        conversion_history.clear()
        st.experimental_rerun()
    
    # Show summary chart
    st.subheader("📊 Conversion Summary")
    fig, ax = plt.subplots()
    df["From"].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)
