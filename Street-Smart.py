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

selected_voice = st.selectbox(
    "Choose a voice",
    [v.name for v in elevenlabs.voices()]
)

questions = [
    {
        "question": "What technique helps align to a straight path?",
        "choices": ["Shorelining", "Trailing", "Square lining"],
        "answer": "Shorelining"},
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


def simulate_crossing():
    return random.choice([True, False])


st.title("Street Crossing Game")

if "points" not in st.session_state:
    st.session_state["points"] = 0

if "streets" not in st.session_state:
    st.session_state["streets"] = 0

st.metric("Points", st.session_state["points"])
st.metric("Streets Crossed", st.session_state["streets"])

col1, col2 = st.columns(2)

with col1:
    if st.button("Cross Street"):

        crossed = simulate_crossing()

        if crossed:

            st.session_state["streets"] += 1
            st.session_state["points"] += 1

            elevenlabs.play(elevenlabs.generate(
                "You crossed the street!", voice=selected_voice))

        else:
            elevenlabs.play(elevenlabs.generate(
                "Unsafe to cross!", voice=selected_voice))
with col2:

    if st.button("Answer Question"):

        q = random.choice(questions)

        elevenlabs.play(elevenlabs.generate(
            q["question"], voice=selected_voice))
        st.write(q["question"])

        selection = st.radio("Select your answer:", q["choices"])
        elevenlabs.play(elevenlabs.generate(f"You selected: {selection}"))

        submit = st.button("Submit Answer")

        if submit:

            if selection == q["answer"]:

                st.session_state["points"] += 10
                st.success("Correct!")

            else:
                st.error("Incorrect!")

st.experimental_rerun()
