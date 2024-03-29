import streamlit as st
from homepage import show_homepage
from chat_pdf import main as pdf_main
from blog2 import blog
from code_exp import code_main
import json
from streamlit_lottie import st_lottie
from PIL import Image

def main():
    #st.set_page_config(page_title="Notescribes", page_icon="icon.png")
    st.title("Notescribes")
     
    st.sidebar.title("Navigation")

    # Display logo in the navigation bar
    pg_icon=Image.open('logo.png')
    st.sidebar.image(pg_icon, use_column_width=True)

    selected_page = st.sidebar.radio("Go to", ["Home", "Insight","Script","Explore"])

    if selected_page == "Home":
        show_homepage()

    elif selected_page == "Insight":
        pdf_main()
    elif selected_page == "Script":
        blog()
    elif selected_page == "Explore":
        code_main()
    

if __name__ == "__main__":
    main()
