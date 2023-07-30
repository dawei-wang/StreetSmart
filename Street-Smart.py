import os
import dotenv
import streamlit as st
import random
import elevenlabs
from elevenlabs import voices

# Load environment variables
dotenv.load_dotenv()

# ElevenLabs setup
api_key = os.getenv("ELEVENLABS_API_KEY")
elevenlabs.set_api_key(api_key)

# Voice selection
voices = elevenlabs.voices()
voice_options = [v.name for v in voices]
selected_voice = st.selectbox(
    "Choose a voice",
    voice_options
)

# Questions
questions = [
    {
        "question": "What technique helps align to a straight path?",
        "choices": ["Shorelining", "Trailing", "Square lining"],
        "answer": "Shorelining"
    },
    {
        "question": "What technique helps cross streets perpendicularly?",
        "choices": ["Route lining", "Shorelining", "Trailing"],
        "answer": "Route lining"
    },
    {
        "question": "What technique involves keeping shoulder aligned to wall?",
        "choices": ["Trailing", "Shorelining", "Route lining"],
        "answer": "Trailing"
    }
]

# Streamlit UI
st.title("Street Crossing Game")
st.metric("Points", 0)
st.metric("Streets Crossed", 0)

# Initialize points and streets
if "points" not in st.session_state:
    st.session_state["points"] = 0

if "streets" not in st.session_state:
    st.session_state["streets"] = 0

col1, col2 = st.columns(2)

with col1:
    if st.button("Cross Street"):
        st.session_state["points"] += 10
        st.session_state["streets"] += 1
        elevenlabs.play(
            elevenlabs.generate("You crossed the street!",
                                voice=selected_voice)
        )

with col2:
    if st.button("Answer Question"):
        q = random.choice(questions)
        # Speak and display question
        elevenlabs.play(elevenlabs.generate(
            q["question"], voice=selected_voice))
        st.write(q["question"])

        # Replay audio
        replay = st.button("Replay Audio")
        if replay:
            elevenlabs.play(elevenlabs.generate(q["question"]))

    # Get user selection
        selection = st.radio(
            "Select your answer:",
            q["choices"]
        )

    # Read back selection
        elevenlabs.play(elevenlabs.generate(f"You selected: {selection}"))

    # Submit answer
    submit = st.button("Submit Answer")
    if submit:

        if selection == q["answer"]:
            st.success("Correct!")
            st.session_state["points"] += 10

        else:
            st.error("Incorrect!")
st.experimental_rerun()
