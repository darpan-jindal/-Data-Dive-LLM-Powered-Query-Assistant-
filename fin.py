import streamlit as st
from PIL import Image  # Import for image handling
from main import getinfo

# Set page config at the beginning of your main script
st.set_page_config(
    page_title="AtliQ T Shirts: Database Q&A",  # Customize as needed
    page_icon=":shirt:",  # Add a shirt icon (optional)
    layout="wide",  # Expand the app to full screen width (optional)
    initial_sidebar_state="collapsed",  # Initially hide the sidebar (optional)
)

# Display image banner (optional)
# Display image banner (optional)
try:
    image = Image.open("OIP (1).jpeg")
    image = image.resize((1410,10))  # Resize the image before displaying
    st.image(image, use_column_width=False)  # Adjust width for a visually appealing size
except FileNotFoundError:
    st.warning("Banner image not found. Please provide a valid image path.")


# Create a vibrant gradient theme (feel free to customize)
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(to right, #FFC0CB, #800080);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center; color: white; text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25); padding: 20px;'>AtliQ T Shirts: Database Q&A</h1>", 
    unsafe_allow_html=True,
)

question = st.text_input(
    "Question: ",
    key="question_input",  # Add a unique key for better caching
    placeholder="Enter your question here...",  # Informative placeholder
)

if question:
    chain = getinfo()
    response = chain(question)

    st.markdown(
        "<h2 style='color: white; font-size: 30px;'>Answer:</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<ul><li style='color: white; font-size: 30px; font-weight: bold;'>{response['result']}</li></ul>",
        unsafe_allow_html=True,
    )
