import streamlit as st
import pandas as pd
import joblib

# Paths to model and dataset
model_path = "./models/meditation_model.pkl"
dataset_path = "./data/meditation.csv"

# Load the model
@st.cache_resource
def load_model():
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load the dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(dataset_path)
        # Ensure all columns are loaded and within range
        required_columns = ['Name', 'Description', 'Duration', 'Instructions', 'mood', 'mindfulness', 'sleep_quality', 'energy_level']
        if not all(col in df.columns for col in required_columns):
            st.error("Dataset is missing required columns.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# Recommendation function
def recommend_meditation(mood, mindfulness, sleep_quality, energy_level, model, data):
    try:
        # Prepare input data as a DataFrame
        user_data = pd.DataFrame({
            'mood': [mood],
            'mindfulness': [mindfulness],
            'sleep_quality': [sleep_quality],
            'energy_level': [energy_level]
        })
        
        # Make prediction
        recommended_name = model.predict(user_data)[0]

        # Retrieve meditation details
        meditation_details = data[data['Name'] == recommended_name].iloc[0]
        return {
            'name': meditation_details['Name'],
            'description': meditation_details['Description'],
            'duration': meditation_details['Duration'],
            'instructions': meditation_details['Instructions']
        }
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return None

# UI for the Meditation Recommender
st.title("Meditation Recommender")

# User inputs
mood = st.selectbox("Mood", ["Stressed", "Anxious", "Happy", "Sad"])
mindfulness = st.slider("Mindfulness (1-5)", 1, 5, 3)
sleep_quality = st.slider("Sleep Quality (1-5)", 1, 5, 3)
energy_level = st.slider("Energy Level (1-5)", 1, 5, 3)

# Load model and data
model = load_model()
data = load_data()

# Display recommendation when button is clicked
if st.button("Get Recommendation"):
    if model is not None and data is not None:
        recommendation = recommend_meditation(mood, mindfulness, sleep_quality, energy_level, model, data)
        if recommendation:
            st.write("### Recommended Meditation")
            st.write(f"**Name:** {recommendation['name']}")
            st.write(f"**Description:** {recommendation['description']}")
            st.write(f"**Duration:** {recommendation['duration']} minutes")
            st.write(f"**Instructions:** {recommendation['instructions']}")
        else:
            st.error("Could not generate a recommendation.")
