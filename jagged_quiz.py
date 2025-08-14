# jagged_quiz_app.py

import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
import math

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

# --- Data for Learning and Career Paths ---
# A dictionary to map each dimension to relevant career and learning paths.
# The content is tailored for teenagers, focusing on relatable concepts and future potential.
LEARNING_PATHS_AND_CAREERS = {
    "Nature & Environment": {
        "learning": [
            "Explore subjects like **Biology**, **Environmental Science**, or **Geology**.",
            "Research topics like **sustainable agriculture**, **conservation**, and **climate science**.",
            "Focus on understanding ecosystems, animal behavior, and the relationship between living things and their environment.",
        ],
        "careers": [
            "**Marine Biologist:** Studying sea life and ocean ecosystems.",
            "**Environmental Scientist:** Finding solutions to pollution and climate issues.",
            "**Urban Planner:** Designing sustainable cities with parks and green spaces.",
            "**Park Ranger:** Protecting and managing natural parks and wildlife."
        ]
    },
    "Numbers & Logic": {
        "learning": [
            "Dive into **Advanced Mathematics**, **Statistics**, or **Formal Logic**.",
            "Learn **Computer Science** and **Algorithmic Thinking** to solve complex problems.",
            "Study **data analysis** and how to use data to spot trends and make informed decisions.",
        ],
        "careers": [
            "**Software Engineer:** Building apps and websites using code.",
            "**Data Scientist:** Finding patterns in data to make important discoveries.",
            "**Financial Analyst:** Helping people and companies manage their money.",
            "**Game Designer:** Using logic and strategy to create video games."
        ]
    },
    "Words & Communication": {
        "learning": [
            "Focus on **English Literature**, **Rhetoric**, and **Creative Writing** to improve your skills.",
            "Study **Journalism** and **Media Studies** to understand how to share ideas with a wider audience.",
            "Take courses in **public speaking** or **debate** to hone your persuasive skills.",
        ],
        "careers": [
            "**Journalist:** Writing stories and reporting on news for a living.",
            "**Marketing Specialist:** Creating messages that get people excited about products.",
            "**Author:** Writing books and creating new worlds.",
            "**Lawyer:** Using powerful words to argue cases and help people."
        ]
    },
    "People & Community": {
        "learning": [
            "Explore subjects like **Sociology**, **Psychology**, and **Social Studies** to understand human behavior.",
            "Learn about **Community Development** and **Public Policy**.",
            "Focus on topics like **conflict resolution**, **group dynamics**, and **cultural diversity**.",
        ],
        "careers": [
            "**Teacher:** Helping students learn and grow in a classroom.",
            "**Social Worker:** Supporting families and individuals in need.",
            "**Human Resources Manager:** Helping people find great jobs and feel happy at work.",
            "**Community Organizer:** Bringing people together to solve local problems."
        ]
    },
    "Making & Building": {
        "learning": [
            "Explore subjects in **Engineering** (mechanical, civil, electrical) and **Physics**.",
            "Learn about **Industrial Design** and **Architecture**.",
            "Focus on hands-on skills like **woodworking**, **robotics**, or **3D modeling**.",
        ],
        "careers": [
            "**Architect:** Designing buildings and structures.",
            "**Engineer:** Creating new machines, gadgets, and systems.",
            "**Web Developer:** Building the visual and functional parts of websites.",
            "**Product Designer:** Inventing and improving everyday products."
        ]
    },
    "Movement & Health": {
        "learning": [
            "Study **Anatomy**, **Physiology**, and **Kinesiology** to understand the human body.",
            "Learn about **Nutrition Science** and how it impacts health.",
            "Explore **Sports Medicine** and **Exercise Science**.",
        ],
        "careers": [
            "**Physical Therapist:** Helping people recover from injuries.",
            "**Personal Trainer:** Guiding others to reach their fitness goals.",
            "**Sports Coach:** Mentoring athletes and developing team strategies.",
            "**Doctor/Nurse:** Working in healthcare to help people stay healthy."
        ]
    },
    "Arts & Creativity": {
        "learning": [
            "Study **Art History**, **Visual Arts**, and **Creative Expression**.",
            "Learn **Music Theory** or **Film Studies**.",
            "Take classes in **graphic design**, **drawing**, or **sculpture** to develop your skills.",
        ],
        "careers": [
            "**Graphic Designer:** Creating visual concepts for brands and media.",
            "**Animator:** Bringing characters and stories to life.",
            "**Musician/Composer:** Creating music and performing.",
            "**Fashion Designer:** Creating new styles of clothing."
        ]
    },
    "Technology & Innovation": {
        "learning": [
            "Explore **Computer Programming** in languages like Python or JavaScript.",
            "Study **AI and Machine Learning** or **Cybersecurity**.",
            "Learn about **User Experience (UX) Design** and **Data Science**.",
        ],
        "careers": [
            "**Cybersecurity Specialist:** Protecting computer systems from hackers.",
            "**AI Developer:** Creating intelligent programs and robots.",
            "**UX/UI Designer:** Making websites and apps easy and fun to use.",
            "**Data Analyst:** Finding valuable insights from large sets of data."
        ]
    },
    "Entrepreneurship & Initiative": {
        "learning": [
            "Take classes in **Business Studies**, **Economics**, or **Marketing**.",
            "Study **Project Management** and **Strategic Planning**.",
            "Learn about **Finance** and the principles of building and managing a business.",
        ],
        "careers": [
            "**Entrepreneur:** Starting and growing your own company.",
            "**Project Manager:** Leading teams to complete projects on time.",
            "**Startup Founder:** Turning a new idea into a successful business.",
            "**Venture Capitalist:** Investing in new and exciting companies."
        ]
    },
    "Critical & Reflective Thinking": {
        "learning": [
            "Engage with **Philosophy**, **Ethics**, and **Formal Logic**.",
            "Study **History** and **Research Methods** to analyze past events and information.",
            "Practice writing **essays** and **analytical papers** to develop your reasoning.",
        ],
        "careers": [
            "**Scientist:** Asking big questions and designing experiments to find answers.",
            "**Researcher:** Investigating topics to discover new knowledge.",
            "**Policy Analyst:** Advising leaders on important decisions.",
            "**Forensic Scientist:** Using critical thinking to solve crimes."
        ]
    },
    "Emotional & Social Intelligence": {
        "learning": [
            "Study **Psychology**, **Sociology**, and **Communication Studies**.",
            "Learn about **Neuroscience** and how emotions are processed in the brain.",
            "Explore **Counseling** and **Social Work** to understand how to help others.",
        ],
        "careers": [
            "**Psychologist:** Helping people understand and manage their emotions.",
            "**Counselor:** Guiding others through difficult life situations.",
            "**Humanitarian Worker:** Providing aid and support to people in crisis.",
            "**Diplomat:** Representing a country and building relationships with other nations."
        ]
    },
    "Digital Media & Creativity": {
        "learning": [
            "Take courses in **Digital Arts**, **Multimedia Production**, and **Animation**.",
            "Learn about **User Experience (UX) Design** and **Interactive Media**.",
            "Focus on subjects like **Film Production**, **Audio Engineering**, and **Graphic Design**.",
        ],
        "careers": [
            "**YouTuber/Content Creator:** Making videos and building a community online.",
            "**Animator:** Bringing characters and stories to life with technology.",
            "**Digital Marketing Manager:** Promoting brands through social media and online ads.",
            "**Video Game Artist:** Creating the visuals for video games."
        ]
    },
    "Scientific Curiosity": {
        "learning": [
            "Explore **Biology**, **Chemistry**, and **Physics** to understand the natural world.",
            "Study **Astronomy** and **Cosmology** to learn about the universe.",
            "Learn about **scientific methods**, **experimental design**, and **data interpretation**.",
        ],
        "careers": [
            "**Biologist:** Studying living organisms and their environments.",
            "**Chemist:** Working with chemicals to create new medicines or materials.",
            "**Astronomer:** Studying stars, planets, and galaxies.",
            "**Geologist:** Exploring the Earth's rocks and natural formations."
        ]
    },
    "Collaborative & Leadership Skills": {
        "learning": [
            "Take courses in **Organizational Behavior** and **Strategic Planning**.",
            "Study **Public Administration** and the role of leadership in community settings.",
            "Learn about **project management** and **effective communication** in a team environment.",
        ],
        "careers": [
            "**CEO/Manager:** Leading a company or a team.",
            "**Team Coach:** Guiding a sports team to victory.",
            "**Military Officer:** Leading a team with discipline and strategy.",
            "**Non-profit Director:** Running an organization that helps others."
        ]
    },
    "Mindfulness & Wellbeing": {
        "learning": [
            "Study **Psychology**, with a focus on **positive psychology** and **cognitive behavioral therapy**.",
            "Explore **Neuroscience** to understand how the brain and body connect.",
            "Learn about **Health Sciences** and **Behavioral Studies**.",
        ],
        "careers": [
            "**Therapist:** Helping people improve their mental health.",
            "**Yoga Instructor:** Teaching others to connect with their body and mind.",
            "**Health Coach:** Guiding people to live healthier lifestyles.",
            "**Wellness Consultant:** Advising companies on how to support their employees' wellbeing."
        ]
    },
}


# --- 2. Session state management ---
# Initialize session state variables on first run
if "page" not in st.session_state:
    st.session_state.page = "quiz"
    st.session_state.responses = {}
    st.session_state.randomized_questions = QUESTIONS_DATA.copy()
    random.shuffle(st.session_state.randomized_questions)
    st.session_state.current_question_index = 0

# --- 3. Quiz page function ---
def show_quiz():
    """Displays the quiz questions and a submit button."""
    # Custom CSS for a more dynamic and colorful title
    st.markdown("""
        <style>
        .title-container {
            text-align: center;
            padding: 20px;
            background-color: #F0F2F6;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .jagged-title {
            color: #4CAF50;
            font-size: 3em;
            font-weight: bold;
        }
        .quiz-description {
            color: #333;
            font-size: 1.2em;
        }
        </style>
        <div class="title-container">
            <h1 class="jagged-title">Jagged Learning Profile Quiz 🧠</h1>
            <p class="quiz-description">Find your unique strengths and see what makes you stand out!</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("---")

    # Get the current question
    current_question_index = st.session_state.current_question_index
    total_questions = len(st.session_state.randomized_questions)
    q_data = st.session_state.randomized_questions[current_question_index]

    # Display progress
    progress_percentage = (current_question_index + 1) / total_questions
    st.progress(progress_percentage)
    st.markdown(f"**Question {current_question_index + 1} of {total_questions}**")

    # Display the single question
    question_text = q_data["question"]
    st.session_state.responses[question_text] = st.radio(
        question_text,
        options=["1 - 😞", "2 - 😐", "3 - 👍", "4 - 😄", "5 - 😎"],
        index=None,
        key=f"q_{current_question_index}",
        horizontal=True
    )
    st.markdown("---")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    # Back button
    with col1:
        if st.session_state.current_question_index > 0:
            if st.button("Back"):
                st.session_state.current_question_index -= 1
                st.rerun()

    # Next / Submit button
    with col3:
        # Check if an answer has been selected for the current question
        has_answered = st.session_state.responses.get(question_text) is not None

        if st.session_state.current_question_index < total_questions - 1:
            if st.button("Next", type="primary", disabled=not has_answered):
                st.session_state.current_question_index += 1
                st.rerun()
        else: # Last question
            if st.button("Submit Quiz", type="primary", disabled=not has_answered):
                st.session_state.page = "results"
                st.rerun()

    # Debug button
    with col4:
        if st.button("Debug: Randomly Complete Quiz"):
            # Reset responses and fill with random choices
            st.session_state.responses = {}
            options = ["1 - 😞", "2 - 😐", "3 - 👍", "4 - 😄", "5 - 😎"]
            for q_data in st.session_state.randomized_questions:
                st.session_state.responses[q_data["question"]] = random.choice(options)
            
            # Transition to the results page
            st.session_state.page = "results"
            st.rerun()

# --- Helper function for the new network chart ---
def create_network_chart(questions_data, dimensions):
    """Generates a plotly network chart to visualize dimension relationships."""
    
    # Calculate the total weight of connections between dimensions
    connections = {}
    for q_data in questions_data:
        primary_dim = q_data["primary_dimension"]
        for secondary_dim, weight in q_data["secondary_weights"].items():
            # Store connections bidirectionally
            if primary_dim != secondary_dim:
                # Use a sorted tuple for the key to handle both directions (A, B) and (B, A)
                key = tuple(sorted((primary_dim, secondary_dim)))
                connections.setdefault(key, 0)
                connections[key] += weight

    # Generate node positions in a circular layout
    num_dimensions = len(dimensions)
    radius = 1.2
    angle_step = 2 * math.pi / num_dimensions
    node_positions = {dim: (radius * math.cos(i * angle_step), radius * math.sin(i * angle_step))
                      for i, dim in enumerate(dimensions)}
    
    # Create lists for the nodes (dimensions)
    node_x = [pos[0] for pos in node_positions.values()]
    node_y = [pos[1] for pos in node_positions.values()]
    node_labels = list(node_positions.keys())

    # Create lists for the edges (connections)
    edge_x = []
    edge_y = []
    line_widths = []
    
    # Get max width for normalization
    max_width = max(connections.values()) if connections else 1
    
    for (dim1, dim2), weight in connections.items():
        x0, y0 = node_positions[dim1]
        x1, y1 = node_positions[dim2]
        
        # Add a line for the edge
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Normalize line width for better visual distinction
        normalized_width = (weight / max_width) * 5
        line_widths.append(normalized_width)

    # Plot the edges
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=line_widths, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Plot the nodes
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        textposition='bottom center',
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            size=20,
            line_width=2),
        text=node_labels
    )
    
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='How Your Strengths Connect',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig


# --- 4. Results page function ---
def show_results():
    """Calculates scores and displays the results page with charts and table."""
    st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: #F0F2F6; border-radius: 10px; margin-bottom: 30px;">
            <h1 style="color: #4CAF50; font-size: 3em; font-weight: bold;">Your Jagged Learning Profile 🚀</h1>
        </div>
    """, unsafe_allow_html=True)
    st.write("---")

    # Initialize scores and maximum possible scores for all dimensions to zero
    scores = {dim: 0 for dim in DIMENSIONS}
    max_scores = {dim: 0 for dim in DIMENSIONS}

    # Calculate scores based on the responses to the randomized questions
    for q_data in st.session_state.randomized_questions:
        question_text = q_data["question"]
        primary_dim = q_data["primary_dimension"]
        secondary_weights = q_data["secondary_weights"]

        # Extract integer value from emoji-enhanced radio button selection
        # Ensure a response exists before trying to access it
        response_str = st.session_state.responses.get(question_text)
        if response_str:
            response = int(response_str.split(' ')[0])

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

    # --- Plotly Network Chart ---
    st.subheader("How Your Strengths Connect")
    st.markdown("This network chart shows the **relationships between different dimensions**. The **thicker the line**, the stronger the connection. This can help you understand how a passion in one area, like `Nature & Environment`, can lead to a related interest, like `Scientific Curiosity`.")
    fig_network = create_network_chart(QUESTIONS_DATA, DIMENSIONS)
    st.plotly_chart(fig_network, use_container_width=True)
    
    st.markdown("---")

    # --- Plotly Radar Chart ---
    st.subheader("Your Learning Profile Overview")
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
        title_text="", # Removed title here to avoid duplication
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
    st.subheader("Top Strengths & Career Paths 🚀")
    top_dims = score_df.head(3)
    st.write("Based on your responses, here are your top three strengths and some ways you can explore them:")

    # Display suggestions for each of the top dimensions
    for _, row in top_dims.iterrows():
        dimension = row['Dimension']
        score = row['Score']
        st.markdown(f"#### **{dimension}** (Score: {score:.2f})")

        # Use an expander to make the content collapsible
        with st.expander("💡 Learning Paths & Subjects"):
            st.markdown("Here are some subjects and fields you can explore:")
            paths = LEARNING_PATHS_AND_CAREERS.get(dimension, {}).get("learning", [])
            for path in paths:
                st.markdown(f"- {path}")

        with st.expander("💼 Potential Career Paths"):
            st.markdown("Your strengths in this area could lead to a career as a:")
            careers = LEARNING_PATHS_AND_CAREERS.get(dimension, {}).get("careers", [])
            for career in careers:
                st.markdown(f"- {career}")

    st.markdown("---")
    if st.button("Restart Quiz"):
        st.session_state.page = "quiz"
        st.session_state.responses = {}
        # Re-randomize questions for the new quiz
        st.session_state.randomized_questions = QUESTIONS_DATA.copy()
        random.shuffle(st.session_state.randomized_questions)
        st.session_state.current_question_index = 0
        st.rerun()


# --- 5. Page navigation logic ---
if st.session_state.page == "quiz":
    show_quiz()
else:
    show_results()
