import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go

st.set_page_config(page_title="Student Learning & Interest Quiz", layout="wide")

# --- Questions & Dimensions ---
questions = [
    ("I enjoy observing animals, plants, or natural environments.", "Nature & Environment"),
    ("I’m curious about how ecosystems and the Earth work.", "Nature & Environment"),
    ("I feel motivated to protect nature and wildlife.", "Nature & Environment"),
    ("I enjoy learning about environmental problems and solutions.", "Nature & Environment"),
    
    ("I enjoy solving challenging puzzles or logic problems.", "Numbers & Logic"),
    ("I like spotting patterns or trends in numbers and data.", "Numbers & Logic"),
    ("I feel confident analyzing information to make decisions.", "Numbers & Logic"),
    ("I enjoy games or activities that require careful planning.", "Numbers & Logic"),
    
    ("I enjoy writing stories, articles, or creative pieces.", "Words & Communication"),
    ("I like explaining ideas so others can understand them.", "Words & Communication"),
    ("I’m interested in how language influences people.", "Words & Communication"),
    ("I enjoy sharing my thoughts through speeches, blogs, or media.", "Words & Communication"),
    
    ("I like helping people overcome challenges or learn new skills.", "People & Community"),
    ("I enjoy working with others to reach a shared goal.", "People & Community"),
    ("I’m interested in understanding how people think and feel.", "People & Community"),
    ("I feel motivated to make a positive difference in my community.", "People & Community"),
    
    ("I enjoy designing or creating objects or systems.", "Making & Building"),
    ("I like improving or fixing things to make them work better.", "Making & Building"),
    ("I feel proud when I build or complete something with my hands.", "Making & Building"),
    ("I enjoy experimenting with ideas to create new things.", "Making & Building"),
    
    ("I enjoy physical activities that challenge my body.", "Movement & Health"),
    ("I’m interested in learning how the body works and stays healthy.", "Movement & Health"),
    ("I like setting goals to improve my fitness or skills.", "Movement & Health"),
    ("I feel energized by sports, dance, or other active challenges.", "Movement & Health"),
    
    ("I enjoy creating art, music, or performance projects.", "Arts & Creativity"),
    ("I like coming up with original ideas or new ways of doing things.", "Arts & Creativity"),
    ("I enjoy experimenting with styles, colors, or artistic techniques.", "Arts & Creativity"),
    ("I feel inspired when imagining or designing something new.", "Arts & Creativity"),
    
    ("I enjoy learning how technology, gadgets, or software work.", "Technology & Innovation"),
    ("I like thinking of ways technology could solve real problems.", "Technology & Innovation"),
    ("I enjoy experimenting with coding, robotics, or digital tools.", "Technology & Innovation"),
    ("I’m curious about inventing or improving technological solutions.", "Technology & Innovation"),
]

dimensions = ["Nature & Environment", "Numbers & Logic", "Words & Communication",
              "People & Community", "Making & Building", "Movement & Health",
              "Arts & Creativity", "Technology & Innovation"]

career_suggestions = {
    "Nature & Environment": "Environmental Science, Ecology, Conservation",
    "Numbers & Logic": "Mathematics, Data Science, Engineering",
    "Words & Communication": "Journalism, Writing, Communications",
    "People & Community": "Psychology, Education, Social Work",
    "Making & Building": "Architecture, Product Design, Engineering",
    "Movement & Health": "Sports Science, Physiotherapy, Health Sciences",
    "Arts & Creativity": "Fine Arts, Graphic Design, Music, Theatre",
    "Technology & Innovation": "Computer Science, Robotics, UX/UI Design"
}

# --- Initialize session state ---
if "responses" not in st.session_state:
    st.session_state.responses = []
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))
if "page" not in st.session_state:
    st.session_state.page = "quiz"

# --- Navigation ---
def go_to_results():
    st.session_state.page = "results"

def go_to_quiz():
    st.session_state.page = "quiz"
    st.session_state.responses = []
    st.session_state.shuffled_questions = random.sample(questions, len(questions))

# --- Quiz Page ---
if st.session_state.page == "quiz":
    st.title("Student Learning & Interest Quiz (12-16)")
    st.subheader("Please rate each statement (1 = Disagree, 5 = Strongly Agree)")
    
    st.session_state.responses = []
    for q_text, _ in st.session_state.shuffled_questions:
        response = st.radio(q_text, [1,2,3,4,5], index=2, horizontal=True)
        st.session_state.responses.append(response)
    
    st.button("Submit Quiz", on_click=go_to_results)
    st.button("Clear All Responses", on_click=go_to_quiz)

# --- Results Page ---
if st.session_state.page == "results":
    st.title("Your Quiz Results")
    
    # Calculate scores
    scores = {dim:0 for dim in dimensions}
    for resp, (_, dim) in zip(st.session_state.responses, st.session_state.shuffled_questions):
        scores[dim] += resp
    
    profile_df = pd.DataFrame({"Dimension": list(scores.keys()), "Score": list(scores.values())})
    st.subheader("Jagged Profile")
    st.dataframe(profile_df)
    
    # Radar chart with Plotly
    categories = list(scores.keys())
    values = list(scores.values())
    values += values[:1]  # close the loop

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name='Score',
        marker_color='skyblue'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,20], tickvals=[0,5,10,15,20])
        ),
        showlegend=False,
        title="Jagged Profile Radar Chart"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top careers
    st.subheader("Top Suggested Areas of Study / Careers")
    top_dims = profile_df.sort_values("Score", ascending=False).head(3)["Dimension"].tolist()
    for dim in top_dims:
        st.write(f"**{dim}:** {career_suggestions[dim]}")
    
    st.button("Take Quiz Again", on_click=go_to_quiz)
