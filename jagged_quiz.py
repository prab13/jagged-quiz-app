# jagged_quiz_app.py

import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go

# Set page configuration for a clean, wide layout
st.set_page_config(page_title="Jagged Learning Profile Quiz", layout="wide")

# --- 1. Data Definitions (a more robust structure using a list of dictionaries) ---
# Each question is a dictionary with clear keys for its properties.
QUESTIONS_DATA = [
    {
        "question": "I enjoy observing animals, plants, or natural environments.",
        "primary_dimension": "Nature & Environment",
        "secondary_weights": {"Scientific Curiosity": 0.4},
    },
    {
        "question": "I am curious about how ecosystems and the Earth work.",
        "primary_dimension": "Nature & Environment",
        "secondary_weights": {"Scientific Curiosity": 0.4},
    },
    {
        "question": "I like learning about environmental problems and ways to solve them.",
        "primary_dimension": "Nature & Environment",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    {
        "question": "I feel motivated to protect nature or wildlife.",
        "primary_dimension": "Nature & Environment",
        "secondary_weights": {"Emotional & Social Intelligence": 0.3},
    },
    # Numbers & Logic
    {
        "question": "I enjoy solving puzzles or logic problems.",
        "primary_dimension": "Numbers & Logic",
        "secondary_weights": {"Critical & Reflective Thinking": 0.4},
    },
    {
        "question": "I like spotting patterns or trends in numbers or data.",
        "primary_dimension": "Numbers & Logic",
        "secondary_weights": {"Scientific Curiosity": 0.4},
    },
    {
        "question": "I feel confident analyzing information to make decisions.",
        "primary_dimension": "Numbers & Logic",
        "secondary_weights": {"Critical & Reflective Thinking": 0.5},
    },
    {
        "question": "I enjoy planning and strategizing in games or projects.",
        "primary_dimension": "Numbers & Logic",
        "secondary_weights": {"Entrepreneurship & Initiative": 0.3},
    },
    # Words & Communication
    {
        "question": "I enjoy writing stories, essays, or articles.",
        "primary_dimension": "Words & Communication",
        "secondary_weights": {"Arts & Creativity": 0.4},
    },
    {
        "question": "I like explaining ideas clearly so others understand them.",
        "primary_dimension": "Words & Communication",
        "secondary_weights": {"Emotional & Social Intelligence": 0.3},
    },
    {
        "question": "I am interested in how words and language influence people.",
        "primary_dimension": "Words & Communication",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    {
        "question": "I enjoy sharing my ideas through speeches, blogs, or media.",
        "primary_dimension": "Words & Communication",
        "secondary_weights": {"Digital Media & Creativity": 0.4},
    },
    # People & Community
    {
        "question": "I enjoy helping others overcome challenges or learn new skills.",
        "primary_dimension": "People & Community",
        "secondary_weights": {"Emotional & Social Intelligence": 0.5},
    },
    {
        "question": "I like working collaboratively to achieve a shared goal.",
        "primary_dimension": "People & Community",
        "secondary_weights": {"Collaborative & Leadership Skills": 0.4},
    },
    {
        "question": "I am curious about understanding how people think and feel.",
        "primary_dimension": "People & Community",
        "secondary_weights": {"Emotional & Social Intelligence": 0.5},
    },
    {
        "question": "I feel motivated to make a positive difference in my community.",
        "primary_dimension": "People & Community",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.3},
    },
    # Making & Building
    {
        "question": "I enjoy designing or creating objects or systems.",
        "primary_dimension": "Making & Building",
        "secondary_weights": {"Technology & Innovation": 0.4},
    },
    {
        "question": "I like improving or fixing things to make them work better.",
        "primary_dimension": "Making & Building",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    {
        "question": "I feel proud when I complete a hands-on project.",
        "primary_dimension": "Making & Building",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.3},
    },
    {
        "question": "I enjoy experimenting with ideas to create new things.",
        "primary_dimension": "Making & Building",
        "secondary_weights": {"Entrepreneurship & Initiative": 0.4},
    },
    # Movement & Health
    {
        "question": "I enjoy physical activities that challenge my body.",
        "primary_dimension": "Movement & Health",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.3},
    },
    {
        "question": "I am interested in learning how the body works and stays healthy.",
        "primary_dimension": "Movement & Health",
        "secondary_weights": {"Scientific Curiosity": 0.3},
    },
    {
        "question": "I like setting goals to improve my fitness or skills.",
        "primary_dimension": "Movement & Health",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.4},
    },
    {
        "question": "I feel energized by sports, dance, or other active challenges.",
        "primary_dimension": "Movement & Health",
        "secondary_weights": {"Emotional & Social Intelligence": 0.3},
    },
    # Arts & Creativity
    {
        "question": "I enjoy creating art, music, or performance projects.",
        "primary_dimension": "Arts & Creativity",
        "secondary_weights": {"Digital Media & Creativity": 0.4},
    },
    {
        "question": "I like coming up with original ideas or new ways of doing things.",
        "primary_dimension": "Arts & Creativity",
        "secondary_weights": {"Entrepreneurship & Initiative": 0.4},
    },
    {
        "question": "I enjoy experimenting with styles, colors, or artistic techniques.",
        "primary_dimension": "Arts & Creativity",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    {
        "question": "I feel inspired when imagining or designing something new.",
        "primary_dimension": "Arts & Creativity",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.3},
    },
    # Technology & Innovation
    {
        "question": "I enjoy learning how technology, gadgets, or software work.",
        "primary_dimension": "Technology & Innovation",
        "secondary_weights": {"Scientific Curiosity": 0.4},
    },
    {
        "question": "I like thinking of ways technology can solve real problems.",
        "primary_dimension": "Technology & Innovation",
        "secondary_weights": {"Entrepreneurship & Initiative": 0.4},
    },
    {
        "question": "I enjoy experimenting with coding, robotics, or digital tools.",
        "primary_dimension": "Technology & Innovation",
        "secondary_weights": {"Digital Media & Creativity": 0.4},
    },
    {
        "question": "I am curious about inventing or improving technological solutions.",
        "primary_dimension": "Technology & Innovation",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    # Entrepreneurship & Initiative
    {
        "question": "I enjoy creating projects or small ventures from an idea.",
        "primary_dimension": "Entrepreneurship & Initiative",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    {
        "question": "I like taking the lead in solving challenges or making improvements.",
        "primary_dimension": "Entrepreneurship & Initiative",
        "secondary_weights": {"Collaborative & Leadership Skills": 0.4},
    },
    {
        "question": "I feel motivated to try new approaches or take calculated risks.",
        "primary_dimension": "Entrepreneurship & Initiative",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.3},
    },
    {
        "question": "I enjoy finding creative solutions to everyday problems.",
        "primary_dimension": "Entrepreneurship & Initiative",
        "secondary_weights": {"Critical & Reflective Thinking": 0.4},
    },
    # Critical & Reflective Thinking
    {
        "question": "I enjoy analyzing why things work the way they do.",
        "primary_dimension": "Critical & Reflective Thinking",
        "secondary_weights": {"Scientific Curiosity": 0.4},
    },
    {
        "question": "I like questioning assumptions to better understand a topic.",
        "primary_dimension": "Critical & Reflective Thinking",
        "secondary_weights": {"Numbers & Logic": 0.3},
    },
    {
        "question": "I enjoy comparing different viewpoints before forming an opinion.",
        "primary_dimension": "Critical & Reflective Thinking",
        "secondary_weights": {"Emotional & Social Intelligence": 0.3},
    },
    {
        "question": "I reflect on my decisions to see how I could improve them.",
        "primary_dimension": "Critical & Reflective Thinking",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.4},
    },
    # Emotional & Social Intelligence
    {
        "question": "I notice how my actions affect other people.",
        "primary_dimension": "Emotional & Social Intelligence",
        "secondary_weights": {"People & Community": 0.4},
    },
    {
        "question": "I enjoy helping friends solve personal or emotional challenges.",
        "primary_dimension": "Emotional & Social Intelligence",
        "secondary_weights": {"People & Community": 0.5},
    },
    {
        "question": "I can understand someone else’s perspective easily.",
        "primary_dimension": "Emotional & Social Intelligence",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    {
        "question": "I am aware of my feelings and can manage them well.",
        "primary_dimension": "Emotional & Social Intelligence",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.4},
    },
    # Digital Media & Creativity
    {
        "question": "I enjoy creating videos, music, or digital artwork.",
        "primary_dimension": "Digital Media & Creativity",
        "secondary_weights": {"Arts & Creativity": 0.4},
    },
    {
        "question": "I like experimenting with apps or tools to express myself creatively.",
        "primary_dimension": "Digital Media & Creativity",
        "secondary_weights": {"Technology & Innovation": 0.4},
    },
    {
        "question": "I am interested in designing or editing digital content.",
        "primary_dimension": "Digital Media & Creativity",
        "secondary_weights": {"Entrepreneurship & Initiative": 0.3},
    },
    {
        "question": "I enjoy combining technology and imagination to make something new.",
        "primary_dimension": "Digital Media & Creativity",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    # Scientific Curiosity
    {
        "question": "I enjoy designing experiments to see what happens.",
        "primary_dimension": "Scientific Curiosity",
        "secondary_weights": {"Critical & Reflective Thinking": 0.4},
    },
    {
        "question": "I ask questions to understand how things in nature or science work.",
        "primary_dimension": "Scientific Curiosity",
        "secondary_weights": {"Nature & Environment": 0.4},
    },
    {
        "question": "I enjoy observing phenomena carefully and recording what I see.",
        "primary_dimension": "Scientific Curiosity",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    {
        "question": "I like testing ideas to see if they really work.",
        "primary_dimension": "Scientific Curiosity",
        "secondary_weights": {"Entrepreneurship & Initiative": 0.3},
    },
    # Collaborative & Leadership Skills
    {
        "question": "I enjoy organizing group activities or projects.",
        "primary_dimension": "Collaborative & Leadership Skills",
        "secondary_weights": {"People & Community": 0.4},
    },
    {
        "question": "I like guiding others to achieve a shared goal.",
        "primary_dimension": "Collaborative & Leadership Skills",
        "secondary_weights": {"Entrepreneurship & Initiative": 0.3},
    },
    {
        "question": "I feel confident taking responsibility for team decisions.",
        "primary_dimension": "Collaborative & Leadership Skills",
        "secondary_weights": {"Mindfulness & Wellbeing": 0.3},
    },
    {
        "question": "I enjoy helping a group work together smoothly.",
        "primary_dimension": "Collaborative & Leadership Skills",
        "secondary_weights": {"Emotional & Social Intelligence": 0.4},
    },
    # Mindfulness & Wellbeing
    {
        "question": "I enjoy practicing mindfulness or reflecting on my feelings.",
        "primary_dimension": "Mindfulness & Wellbeing",
        "secondary_weights": {"Emotional & Social Intelligence": 0.4},
    },
    {
        "question": "I pay attention to my wellbeing and daily habits.",
        "primary_dimension": "Mindfulness & Wellbeing",
        "secondary_weights": {"Movement & Health": 0.4},
    },
    {
        "question": "I can stay focused and calm even in challenging situations.",
        "primary_dimension": "Mindfulness & Wellbeing",
        "secondary_weights": {"Critical & Reflective Thinking": 0.3},
    },
    {
        "question": "I take time to think about my strengths and areas I want to improve.",
        "primary_dimension": "Mindfulness & Wellbeing",
        "secondary_weights": {"Critical & Reflective Thinking": 0.4},
    },
]

# A set of all unique dimensions for initialization
DIMENSIONS = sorted(list(set([q["primary_dimension"] for q in QUESTIONS_DATA] + [dim for q in QUESTIONS_DATA for dim in q["secondary_weights"]])))

# --- 2. Session state management ---
# Initialize session state variables on first run
if "page" not in st.session_state:
    st.session_state.page = "quiz"
    st.session_state.responses = {}
    st.session_state.randomized_questions = QUESTIONS_DATA.copy()
    random.shuffle(st.session_state.randomized_questions)

# --- 3. Quiz page function ---
def show_quiz():
    """Displays the quiz questions and a submit button."""
    st.title("Jagged Learning Profile Quiz")
    st.write("Select the option that best describes you for each statement (1 = Disagree, 5 = Strongly Agree).")

    # Use a unique key for each question based on its content, not its index
    for q_data in st.session_state.randomized_questions:
        question_text = q_data["question"]
        st.session_state.responses[question_text] = st.radio(
            question_text,
            options=[1, 2, 3, 4, 5],
            index=st.session_state.responses.get(question_text, 3) - 1,
            key=question_text,
            horizontal=True # Display radio buttons horizontally for better layout
        )

    st.markdown("---")
    if st.button("Submit Quiz"):
        st.session_state.page = "results"

# --- 4. Results page function ---
def show_results():
    """Calculates scores and displays the results page with a radar chart and table."""
    st.title("Your Jagged Learning Profile")

    # Initialize scores and maximum possible scores for all dimensions to zero
    scores = {dim: 0 for dim in DIMENSIONS}
    max_scores = {dim: 0 for dim in DIMENSIONS}

    # Calculate scores based on the responses to the randomized questions
    for q_data in st.session_state.randomized_questions:
        question_text = q_data["question"]
        primary_dim = q_data["primary_dimension"]
        secondary_weights = q_data["secondary_weights"]

        # Safely get the response, defaulting to 3 if not found
        response = st.session_state.responses.get(question_text, 3)

        # Apply scoring for primary dimension
        scores[primary_dim] += response
        max_scores[primary_dim] += 5

        # Apply scoring for secondary dimensions
        for sec_dim, weight in secondary_weights.items():
            scores[sec_dim] += response * weight
            max_scores[sec_dim] += 5 * weight

    # Normalize scores by dividing the raw score by the maximum possible score for that dimension,
    # then scaling the result to be between 1 and 5. This prevents scores from exceeding 5.
    scores_normalized = {
        dim: (scores[dim] / max_scores[dim]) * 5
        for dim in DIMENSIONS if max_scores[dim] > 0
    }

    # --- Plotly Radar Chart ---
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=list(scores_normalized.values()),
        theta=list(scores_normalized.keys()),
        fill='toself',
        name='Learning Profile'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
        showlegend=False,
        title_text="Your Learning Profile Overview",
        title_x=0.5 # Center the title
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # --- Results Table ---
    st.subheader("Your Scores per Dimension")
    score_df = pd.DataFrame(
        list(scores_normalized.items()), columns=["Dimension", "Score"]
    )
    score_df = score_df.sort_values("Score", ascending=False)
    # Display the table with a clean index and formatted score
    st.dataframe(score_df.style.format({"Score": "{:.2f}"}), use_container_width=True)

    # --- Top Strengths Summary ---
    st.subheader("Top Strengths")
    top_dims = score_df.head(3)
    st.write("Based on your responses, your top three strengths are:")
    for _, row in top_dims.iterrows():
        st.write(f"- **{row['Dimension']}** (Score: {row['Score']:.2f})")

    st.markdown("---")
    if st.button("Restart Quiz"):
        st.session_state.page = "quiz"
        st.session_state.responses = {}
        # Re-randomize questions for the new quiz
        st.session_state.randomized_questions = QUESTIONS_DATA.copy()
        random.shuffle(st.session_state.randomized_questions)


# --- 5. Page navigation logic ---
if st.session_state.page == "quiz":
    show_quiz()
else:
    show_results()
