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
    # (question_text, primary_dimension, {secondary_dimension: weight})
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
    ("I notice how my actions affect other people.", "Emotional & Social Intellig
