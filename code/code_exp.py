#code explanation with only links

import streamlit as st
from googlesearch import search

import json
from streamlit_lottie import st_lottie

# Function to search for explanations online
def search_explanation(query):
    # Perform a Google search
    search_results = list(search(query, num=3, stop=3, pause=2))
    return search_results

# Main function to run the Streamlit app
def code_main():
    st.title("📡 Code Explanation Generator")

    #Animation
    # Load Lottie animation
    def load_lottiefile2(filepath:str):
        with open(filepath,"r") as f:
            return json.load(f)
            
    lottie_code = load_lottiefile2("D:\\Projects\\pdf3\\templates\\code_anim.json")

    # Display Lottie animation (logo) 
    st.markdown(
        """
        <style>
        .logo-container {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 100px; /* Adjust the width as needed */
            height: 100px; /* Adjust the height as needed */
        }
        </style>
        """
    , unsafe_allow_html=True)

    # Add a container div with the logo-container class
    st.markdown("<div class='logo-container'></div>", unsafe_allow_html=True)
        
    # Display the Lottie animation inside the container
    st_lottie(lottie_code, quality="high", width=100, height=100)


    #content
    # User input for code snippet upload
    st.subheader("Upload Your Code Snippet")
    uploaded_file = st.file_uploader("Choose a Python file", type="py")

    # If a file is uploaded
    if uploaded_file is not None:
        # Read the content of the uploaded file
        code = uploaded_file.getvalue().decode("utf-8")

        # Display the uploaded code snippet
        st.subheader("Uploaded Code Snippet")
        st.code(code)

        # Search for explanation for the code snippet
        query = "Explanation for Python code: " + code
        explanation_links = search_explanation(query)

        # Display the generated explanation links
        st.subheader("Explanation Links")
        if explanation_links:
            for link in explanation_links:
                st.write(link)
        else:
            st.write("No explanations found online. Please provide a more specific query.")


