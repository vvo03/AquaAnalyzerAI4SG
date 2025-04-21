import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_water_quality_alert(quality_metric):
    prompt = f"""
    You are an AI assistant specialized in water quality analysis, focusing on pH levels.
    Given this pH value: {quality_metric},
    determine whether it falls within the safe range for human consumption (6.5 to 8.5).
    Clearly explain the implications of this pH level—whether it is too acidic, neutral, or too alkaline.
    Describe any health risks or benefits associated with water of this pH level in simple language for the general public.
    Conclude with a recommendation for whether the water is safe to drink or if action is needed.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

st.title("🔔 Water Quality Notification System")
st.subheader("Understand Your Water's pH Level")
#used chat got to generate ideas on how to explain ph levels to anyone who is unaware of that knowledge and for help for mardown placements
st.markdown("""
**What is pH and why does it matter?**  
pH is a measure of how acidic or alkaline your water is, on a scale from 0 (very acidic) to 14 (very alkaline).  
For drinking water, the ideal range is **6.5 to 8.5**.  
- Low pH can cause corrosion in pipes and may release metals into the water.  
- High pH can make water taste bitter or reduce disinfection effectiveness.  
Understanding your water’s pH helps ensure it's safe, healthy, and pleasant to use.
""")

st.markdown("### March 2024 pH Levels from Treatment Plants")

source_choice = st.selectbox(
    "Select which pH source to analyze:",
    ("PWTP Influent (8.4)", "PWTP Treated (7.7)", "RWTP Influent (8.2)", "RWTP Treated (7.6)")
)

pH_value_map = {
    "PWTP Influent (8.4)": 8.4,
    "PWTP Treated (7.7)": 7.7,
    "RWTP Influent (8.2)": 8.2,
    "RWTP Treated (7.6)": 7.6
}

selected_ph = pH_value_map[source_choice]

if st.button("Generate Alert"):
    alert_message = generate_water_quality_alert(selected_ph)
    st.markdown("### Water Quality Alert")
    st.write(alert_message)

