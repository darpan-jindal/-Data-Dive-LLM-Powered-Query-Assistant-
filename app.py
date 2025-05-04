import streamlit as st
from PIL import Image
from main import getinfo

# Set page config
st.set_page_config(
    page_title="Car Shop",
    page_icon=":car:",
    layout="wide",
)

# Set the background and text color
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(to right, #FFC0CB, #800080);
        color: #FFFFFF;
        font-size: 30px;  # Increase the font size
        font-weight: bold;  # Make the text bold
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a title and center align it
st.markdown(
    "<h1 style='text-align: center; padding: 20px;'>Car Shop</h1>",
    unsafe_allow_html=True,
)

# Add a sidebar for user inputs
with st.sidebar:
    st.header("Ask a Question")
    question = st.text_input(
        "",
        key="question_input",
        placeholder="Enter your question here...",
    )
    # Add an image to the sidebar
    st.image("1.jpg")  # Replace with your image path

# Process the question when the user presses the 'Submit' button
if st.sidebar.button("Submit"):
    chain = getinfo()
    response = chain.run(question)

    st.header("Answer")
    # Display the answer in a list format
    st.write(f"* {response}")
st.markdown(
    """
    <footer style='text-align: center; padding: 20px;'>
        <p>© 2024 Car Shop</p>
        <p>Made by Darpan</p>  # Add text in the last
    </footer>
    """,
    unsafe_allow_html=True,
)
