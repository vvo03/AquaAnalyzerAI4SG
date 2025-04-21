import streamlit as st
import requests
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# March 2025 Water Quality Summary from OCR
def fetch_san_jose_water_data():
    return """• Water system: Santa Clara Valley Water District (ID: 4310027)
• Sampling Period: March 2025
• 204 routine samples collected; 0 Total Coliform positives, 0 E. coli positives
• No repeat samples were required due to absence of positive results
• Total Coliform positive rate: 0.00%
• No E. coli MCL violations occurred
• No Level 1 or Level 2 Treatment Technique assessments were triggered
• Compliance maintained with Revised Total Coliform Rule for the month"""

def get_water_quality_advisory(quality_data):
    system_prompt = (
        "You're an expert water quality analyst. Analyze the following San Jose water data and provide a plain-language summary "
        "of the top 5 concerns and top 5 recommendations. Keep it beginner-friendly and relevant to local residents."
    )
    user_input = f"San Jose Water Quality Data: {quality_data}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]
    )
    return response.choices[0].message.content

# --- Streamlit UI ---
st.title("San Jose Water Quality Advisory")
st.subheader("AI-powered summary of local water safety and recommendations (March 2025 Data)")

if st.button("Check San Jose Water Quality"):
    quality_data = fetch_san_jose_water_data()
    advisory = get_water_quality_advisory(quality_data)
    
    st.write("### Water Quality Report Summary")
    st.write(advisory)

    st.markdown("Was this information helpful?")
    st.feedback("thumbs")
