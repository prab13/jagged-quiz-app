# jagged_quiz_app.py

import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go

st.set_page_config(page_title="Jagged Learning Profile Quiz", layout="wide")

# -----------------------------
# 1. Define questions with weights
# -----------------------------
questions_data = [
    ("I enjoy observing animals, plants, or natural environments.", "Nature & Environment", {"Scientific Curiosity": 0.4}),
    ("I am curious about how ecosystems and the Earth work.", "Nature & Environment", {"Scientific Curiosity": 0.4}),
    ("I like learning about environmental problems and ways to solve them.", "Nature & Environment", {"Critical & Reflective Thinking": 0.3}),
    ("I feel motivated to protect nature or wildlife.", "Nature & Environment", {"Emotional & Social Intelligence": 0.3}),
    # Numbers & Logic
    ("I enjoy solving puzzles or logic problems.", "Numbers & Logic", {"Critical & Reflective Thinking": 0.4}),
    ("I like spotting patterns or trends in numbers or data.", "Numbers & Logic", {"Scientific Curiosity": 0.4}),
    ("I feel confident analyzing information to make decisions.", "Numbers & Logic", {"Critical & Reflective Thinking": 0.5}),
    ("I enjoy planning and strategizing in games or projects.", "Numbers & Logic", {"Entrepreneurship & Initiative": 0.3}),
    # Words & Communication
    ("I enjoy writing stories, essays, or articles.", "Words & Communication", {"Arts & Creativity": 0.4}),
    ("I like explaining ideas clearly so others understand them.", "Words & Communication", {"Emotional & Social Intelligence": 0.3}),
    ("I am interested in how words and language influence people.", "Words & Communication", {"Critical & Reflective Thinking": 0.3}),
    ("I enjoy sharing my ideas through speeches, blogs, or media.", "Words & Communication", {"Digital Media & Creativity": 0.4}),
    # People & Community
    ("I enjoy helping others overcome challenges or learn new skills.", "People & Community", {"Emotional & Social Intelligence": 0.5}),
    ("I like working collaboratively to achieve a shared goal.", "People & Community", {"Collaborative & Leadership Skills": 0.4}),
    ("I am curious about understanding how people think and feel.", "People & Community", {"Emotional & Social Intelligence": 0.5}),
    ("I feel motivated to make a positive difference in my community.", "People & Community", {"Mindfulness & Wellbeing": 0.3}),
    # Making & Building
    ("I enjoy designing or creating objects or systems.", "Making & Building", {"Technology & Innovation": 0.4}),
    ("I like improving or fixing things to make them work better.", "Making & Building", {"Critical & Reflective Thinking": 0.3}),
    ("I feel proud when I complete a hands-on project.", "Making & Building", {"Mindfulness & Wellbeing": 0.3}),
    ("I enjoy experimenting with ideas to create new things.", "Making & Building", {"Entrepreneurship & Initiative": 0.4}),
    # Movement & Health
    ("I enjoy physical activities that challenge my body.", "Movement & Health", {"Mindfulness & Wellbeing": 0.3}),
    ("I am interested in learning how the body works and stays healthy.", "Movement & Health", {"Scientific Curiosity": 0.3}),
    ("I like setting goals to improve my fitness or skills.", "Movement & Health", {"Mindfulness & Wellbeing": 0.4}),
    ("I feel energized by sports, dance, or other active challenges.", "Movement & Health", {"Emotional & Social Intelligence": 0.3}),
    # Arts & Creativity
    ("I enjoy creating art, music, or performance projects.", "Arts & Creativity", {"Digital Media & Creativity": 0.4}),
    ("I like coming up with original ideas or new ways of doing things.", "Arts & Creativity", {"Entrepreneurship & Initiative": 0.4}),
    ("I enjoy experimenting with styles, colors, or artistic techniques.", "Arts & Creativity", {"Critical & Reflective Thinking": 0.3}),
    ("I feel inspired when imagining or designing something new.", "Arts & Creativity", {"Mindfulness & Wellbeing": 0.3}),
    # Technology & Innovation
    ("I enjoy learning how technology, gadgets, or software work.", "Technology & Innovation", {"Scientific Curiosity": 0.4}),
    ("I like thinking of ways technology can solve real problems.", "Technology & Innovation", {"Entrepreneurship & Initiative": 0.4}),
    ("I enjoy experimenting with coding, robotics, or digital tools.", "Technology & Innovation", {"Digital Media & Creativity": 0.4}),
    ("I am curious about inventing or improving technological solutions.", "Technology & Innovation", {"Critical & Reflective Thinking": 0.3}),
    # Entrepreneurship & Initiative
    ("I enjoy creating projects or small ventures from an idea.", "Entrepreneurship & Initiative", {"Critical & Reflective Thinking": 0.3}),
    ("I like taking the lead in solving challenges or making improvements.", "Entrepreneurship & Initiative", {"Collaborative & Leadership Skills": 0.4}),
    ("I feel motivated to try new approaches or take calculated risks.", "Entrepreneurship & Initiative", {"Mindfulness & Wellbeing": 0.3}),
    ("I enjoy finding creative solutions to everyday problems.", "Entrepreneurship & Initiative", {"Critical & Reflective Thinking": 0.4}),
    # Critical & Reflective Thinking
    ("I enjoy analyzing why things work the way they do.", "Critical & Reflective Thinking", {"Scientific Curiosity": 0.4}),
    ("I like questioning assumptions to better understand a topic.", "Critical & Reflective Thinking", {"Numbers & Logic": 0.3}),
    ("I enjoy comparing different viewpoints before forming an opinion.", "Critical & Reflective Thinking", {"Emotional & Social Intelligence": 0.3}),
    ("I reflect on my decisions to see how I could improve them.", "Critical & Reflective Thinking", {"Mindfulness & Wellbeing": 0.4}),
    # Emotional & Social Intelligence
    ("I notice how my actions affect other people.", "Emotional & Social Intelligence", {"People & Community": 0.4}),
    ("I enjoy helping friends solve personal or emotional challenges.", "Emotional & Social Intelligence", {"People & Community": 0.5}),
    ("I can understand someone else’s perspective easily.", "Emotional & Social Intelligence", {"Critical & Reflective Thinking": 0.3}),
    ("I am aware of my feelings and can manage them well.", "Emotional & Social Intelligence", {"Mindfulness & Wellbeing": 0.4}),
    # Digital Media & Creativity
    ("I enjoy creating videos, music, or digital artwork.", "Digital Media & Creativity", {"Arts & Creativity": 0.4}),
    ("I like experimenting with apps or tools to express myself creatively.", "Digital Media & Creativity", {"Technology & Innovation": 0.4}),
    ("I am interested in designing or editing digital content.", "Digital Media & Creativity", {"Entrepreneurship & Initiative": 0.3}),
    ("I enjoy combining technology and imagination to make something new.", "Digital Media & Creativity", {"Critical & Reflective Thinking": 0.3}),
    # Scientific Curiosity
    ("I enjoy designing experiments to see what happens.", "Scientific Curiosity", {"Critical & Reflective Thinking": 0.4}),
    ("I ask questions to understand how things in nature or science work.", "Scientific Curiosity", {"Nature & Environment": 0.4}),
    ("I enjoy observing phenomena carefully and recording what I see.", "Scientific Curiosity", {"Critical & Reflective Thinking": 0.3}),
    ("I like testing ideas to see if they really work.", "Scientific Curiosity", {"Entrepreneurship & Initiative": 0.3}),
    # Collaborative & Leadership Skills
    ("I enjoy organizing group activities or projects.", "Collaborative & Leadership Skills", {"People & Community": 0.4}),
    ("I like guiding others to achieve a shared goal.", "Collaborative & Leadership Skills", {"Entrepreneurship & Initiative": 0.3}),
    ("I feel confident taking responsibility for team decisions.", "Collaborative & Leadership Skills", {"Mindfulness & Wellbeing": 0.3}),
    ("I enjoy helping a group work together smoothly.", "Collaborative & Leadership Skills", {"Emotional & Social Intelligence": 0.4}),
    # Mindfulness & Wellbeing
    ("I enjoy practicing mindfulness or reflecting on my feelings.", "Mindfulness & Wellbeing", {"Emotional & Social Intelligence": 0.4}),
    ("I pay attention to my wellbeing and daily habits.", "Mindfulness & Wellbeing", {"Movement & Health": 0.4}),
    ("I can stay focused and calm even in challenging situations.", "Mindfulness & Wellbeing", {"Critical & Reflective Thinking": 0.3}),
    ("I take time to think about my strengths and areas I want to improve.", "Mindfulness & Wellbeing", {"Critical & Reflective Thinking": 0.4}),
]

dimensions = [
    "Nature & Environment", "Numbers & Logic", "Words & Communication", "People & Community",
    "Making & Building", "Movement & Health", "Arts & Creativity", "Technology & Innovation",
    "Entrepreneurship & Initiative", "Critical & Reflective Thinking", "Emotional & Social Intelligence",
    "Digital Media & Creativity", "Scientific Curiosity", "Collaborative & Leadership Skills",
    "Mindfulness & Wellbeing"
]

# -----------------------------
# 2. Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "quiz"
    st.session_state.responses = {}

# -----------------------------
# 3. Quiz page
# -----------------------------
def show_quiz():
    st.title("Jagged Learning Profile Quiz")
    st.write("Select the option that best describes you for each statement (1 = Disagree, 5 = Strongly Agree).")

    randomized_questions = questions_data.copy()
    random.shuffle(randomized_questions)

    for idx, (question, _, _) in enumerate(randomized_questions):
        key = f"q_{idx}"
        st.session_state.responses[key] = st.radio(
            question, options=[1, 2, 3, 4, 5],
            index=st.session_state.responses.get(key, 3)-1 if st.session_state.responses.get(key) else 2,
            key=key
        )

    if st.button("Submit Quiz"):
        st.session_state.page = "results"

# -----------------------------
# 4. Results page with radar + heatmap
# -----------------------------
def show_results():
    st.title("Your Jagged Learning Profile")

    scores = {dim:0 for dim in dimensions}
    overlap_matrix = pd.DataFrame(0, index=dimensions, columns=dimensions)

    for idx, (question, primary, secondary_dict) in enumerate(questions_data):
        key = f"q_{idx}"
        response = st.session_state.responses.get(key, 3)
        scores[primary] += response
        for sec_dim, weight in secondary_dict.items():
            scores[sec_dim] += response * weight
            overlap_matrix.loc[primary, sec_dim] += response * weight

    scores_normalized = {dim: scores[dim]/4 for dim in scores}

    # Radar chart
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=list(scores_normalized.values()),
        theta=list(scores_normalized.keys()),
        fill='toself',
        name='Learning Profile'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,5])),
        showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Heatmap
    fig_heat = go.Figure(data=go.Heatmap(
        z=overlap_matrix.values,
        x=overlap_matrix.columns,
        y=overlap_matrix.index,
        colorscale='Viridis',
        colorbar=dict(title="Weighted Contribution")
    ))
    fig_heat.update_layout(title="Dimension Overlap Heatmap")
    st.plotly_chart(fig_heat, use_container_width=True)

    top_dims = sorted(scores_normalized.items(), key=lambda x:x[1], reverse=True)[:3]
    st.write("Your top 3 strengths may indicate potential areas for learning and development:")
    for dim, val in top_dims:
        st.write(f"- **{dim}** (score: {val:.2f})")

    if st.button("Restart Quiz"):
        st.session_state.page = "quiz"
        st.session_state.responses = {}

# -----------------------------
# 5. Page navigation
# -----------------------------
if st.session_state.page == "quiz":
    show_quiz()
else:
    show_results()
