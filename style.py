import streamlit as st

def set_custom_css():
    # This function defines custom CSS styles
    # Set the page layout to wide mode
    #st.set_page_config(layout="wide")
    st.markdown("""
    <style>
        .stAppHeader{
            display: None;
        }    
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>   
            .stMainBlockContainer.block-container.st-emotion-cache-yw8pof.ekr3hml4{
                padding: 1rem;
            }     
        </style>
        """, unsafe_allow_html=True)
