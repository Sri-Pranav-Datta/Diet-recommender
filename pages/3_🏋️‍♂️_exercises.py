import streamlit as st
import sqlalchemy
from sqlalchemy import text
from models.fit import *

st.set_page_config(page_title='Eat & Fit', page_icon='images/logo.png')

# Styling for the page
st.markdown(
    f"""
        <style>
            .css-18ni7ap.e8zbici2 {{ opacity: 0 }}
            .css-h5rgaw.egzxvld1 {{ opacity: 0 }}
            .block-container.css-91z34k.egzxvld4 {{
                width: 100%;
                padding: 0.5rem 1rem 10rem;
                max-width: none;
            }}
            .css-uc76bn.e1fqkh3o9 {{
                padding-top: 2rem;
                padding-bottom: 0.25rem;
            }}
        </style>
    """, unsafe_allow_html=True
)

# Centered logo and title
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([0.5, 0.5, 1, 0.75, 1, 0.75, 0.5, 0.5])
with col4:
    st.image(image='images/logo.png', width=140)
with col5:
    st.markdown("""<br/><h1 style="font-size: 30px;">Healthy & Wealthy</h1>
                    <i style="font-size: 15px;">Health & wellness Guide</i>
                """, unsafe_allow_html=True)

# Database connection setup
engine = sqlalchemy.create_engine("sqlite:///database/eatandfit.db")

# Exercise keywords setup
exercise_keywords = ['',]
with engine.connect() as conn:
    query = text("SELECT * FROM Exercise")
    all_exercise_results = conn.execute(query).fetchall()
    exercise_keywords.extend([Exercise(*e).name for e in all_exercise_results])

# Exercise Browser UI
col1, col2, col3 = st.columns([0.4, 1.2, 0.4])
with col2:
    st.markdown("<h1 style='text-align: center'>Exercise Browser</h1>", unsafe_allow_html=True)
    exercise_keyword = st.selectbox("**Search**", tuple(exercise_keywords))

# Display selected exercise
if exercise_keyword:
    with engine.connect() as conn:
        query = text("SELECT * FROM Exercise WHERE Name = :name")
        exercise_result = conn.execute(query, {'name': exercise_keyword}).fetchone()

        if exercise_result:
            exercise = Exercise(*exercise_result)

            # Display Exercise Details
            st.markdown(f"<h2 style='text-align: center'>{exercise.name}</h2>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns([0.15, 1.7, 0.15])
            with col2:
                st.markdown(
                    f"""
                    <iframe width="100%" height="500px" allow="fullscreen;" src="{exercise.link}"></iframe>
                    """, unsafe_allow_html=True
                )
                st.subheader("I. Overview")
                st.markdown("".join(f"<p style='padding-left: 22px'>{p}</p>" for p in exercise.get_overview_paragraph()), unsafe_allow_html=True)

                st.subheader("II. Instructions")
                st.markdown("<ul style='list-style-type: decimal; padding-left: 22px'>" +
                            "".join(f"<li>{li}</li>" for li in exercise.get_introductions_detail()) +
                            "</ul>", unsafe_allow_html=True)
