import streamlit as st
from PIL import Image, ImageDraw
import os
from openai import OpenAI


client = os.environ["OPENAI_API_KEY"]

def get_image(prompt, model="dall-e-3"):
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    return image_url

st.title("Where you pH Lies")
st.subheader("Understand Your Water's pH Level")

# used chat got to generate ideas on how to explain ph levels to anyone who is unaware of that knowledge and for help for markdown placements
st.markdown("""
**What is pH and why does it matter?**  
pH is a measure of how acidic or alkaline your water is, on a scale from 0 (very acidic) to 14 (very alkaline).  
For drinking water, the ideal range is **6.5 to 8.5**.  
- Low pH can cause corrosion in pipes and may release metals into the water. These metals are harmful to consume, especially for children.  
- High pH can make water taste bitter or reduce disinfection effectiveness. Alkaline water is water above a pH level 7, which is less bitter, improves hydration, and relieves people from acid reflux symptoms.    

Understanding your water’s pH helps ensure it's safe, healthy, and pleasant to use. 
A balanced pH in drinking water is crucial for human health because it affects water's safety and taste,
and it can impact the body's ability to absorb minerals and the potential for contamination
""")

st.markdown("### March 2024 pH PWTP Levels from Treatment Plant")

st.markdown("""
On this page, you’ll see a real pH scale that ranges from 0 to 14. You can move the slider to select a pH value, 
and when you click the button, a red marker will appear on the scale to show exactly where your 
selected pH lies. This helps you easily see if your water is considered acidic, neutral, or alkaline, 
based on an official reference chart, without needing to guess or read complicated numbers.
It is defaulted to the PH level of March
""")

# Default pH value from the March report
default_ph = 7.7

user_ph = st.slider(
    "PWTP Treated pH Value (adjust if desired):",
    min_value=0.0,
    max_value=14.0,
    value=default_ph,
    step=0.1
)

if st.button("Generate Visualization"):
    BASE_DIR = os.path.dirname(__file__)
    image_path = os.path.join(BASE_DIR, "image", "ph_scale.png")
   
    # Load the stored static image
    ph_scale_img = Image.open("/Users/megantrang/Team Gold/pages/image/ph_scale.png")
    img_with_marker = ph_scale_img.copy()
    draw = ImageDraw.Draw(img_with_marker)
    
    img_width, img_height = img_with_marker.size
    x_pos = int((user_ph / 14) * img_width)  
    y_pos = int(img_height * 0.4)  

    radius = 10  
    draw.ellipse((x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius), fill="red")

    st.image(img_with_marker, caption=f"Marker showing selected pH value: {user_ph}")