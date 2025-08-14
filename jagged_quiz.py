import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Student Learning & Interest Quiz (12-16)")

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

# --- Clear Responses Button ---
if "responses" not in st.session_state:
    st.session_state.responses = [3]*32

if st.button("Clear All Responses"):
    st.session_state.responses = [3]*32

# --- Display Questions ---
st.subheader("Please rate each statement (1 = Disagree, 5 = Strongly Agree)")
for i, (q, _) in enumerate(questions):
    st.session_state.responses[i] = st.slider(q, 1, 5, value=st.session_state.responses[i])

# --- Calculate Scores ---
scores = {dim:0 for dim in dimensions}
for resp, (_, dim) in zip(st.session_state.responses, questions):
    scores[dim] += resp

# --- Show Jagged Profile ---
st.subheader("Jagged Profile")
profile_df = pd.DataFrame({"Dimension": list(scores.keys()), "Score": list(scores.values())})
st.dataframe(profile_df)

# --- Bar Chart ---
fig, ax = plt.subplots(figsize=(8,5))
ax.barh(profile_df["Dimension"], profile_df["Score"], color='skyblue')
ax.set_xlim(0, 20)
ax.set_xlabel("Score (Max 20)")
ax.set_title("Jagged Profile")
st.pyplot(fig)

# --- Top Career Suggestions ---
st.subheader("Top Suggested Areas of Study / Careers")
top_dims = profile_df.sort_values("Score", ascending=False).head(3)["Dimension"].tolist()
for dim in top_dims:
    st.write(f"**{dim}:** {career_suggestions[dim]}")
