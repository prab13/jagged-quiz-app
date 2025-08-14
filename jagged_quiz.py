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

# --- Data for Learning and Career Paths ---
# A dictionary to map each dimension to relevant career and learning paths.
# The content is tailored for teenagers, focusing on relatable concepts and future potential.
LEARNING_PATHS_AND_CAREERS = {
    "Nature & Environment": {
        "learning": [
            "Join a nature club or a gardening group. 🌱",
            "Start a mini-project on recycling or composting at home. ♻️",
            "Learn about different animal or plant species in your local area. 🌲",
            "Watch documentaries about climate change and ecosystems. 🌍",
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
            "Try solving logic puzzles like Sudoku or nonograms. 🧩",
            "Learn a basic coding language like Python to solve math problems. 🐍",
            "Play strategy games like chess or Go. ♟️",
            "Take online courses in basic statistics or data analysis. 📊",
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
            "Start a blog or a YouTube channel about a topic you love. ✍️",
            "Join a debate club or a school newspaper. 🗣️",
            "Read different genres of books and try to write a review. 📚",
            "Practice public speaking by giving presentations to friends or family. 🎤",
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
            "Volunteer for a local charity or community event. ❤️",
            "Organize a study group or a social club with your friends. 🤝",
            "Practice being an active listener by paying close attention to others. 👂",
            "Read books about psychology and social dynamics. 🧑‍🤝‍🧑",
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
            "Learn to build things with LEGO, wood, or other materials. 🧱",
            "Take a workshop on robotics or electronics. 🤖",
            "Fix something broken around the house, like a chair or a bike. 🛠️",
            "Watch tutorials on how things are made or designed. 🏗️",
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
            "Try a new sport or dance class. 🤸",
            "Learn about nutrition and how to make healthy snacks. 🍎",
            "Set a fitness goal and track your progress. 🏃",
            "Explore mindfulness or yoga to connect with your body. 🧘",
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
            "Start drawing, painting, or sculpting. 🎨",
            "Write songs or learn to play a musical instrument. 🎸",
            "Explore graphic design by creating posters or logos. ✍️",
            "Try acting in a school play or making your own short films. 🎬",
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
            "Join a coding club or robotics team. 💻",
            "Learn to use new software or apps for creative projects. 📲",
            "Try building a simple website or an app. 🌐",
            "Research and experiment with AI or virtual reality tools. 🤖",
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
            "Start a small business like a lemonade stand or a dog-walking service. 💰",
            "Organize a fundraising event for a cause you care about. 📈",
            "Brainstorm ideas for products or services that could solve problems. 💡",
            "Read about famous innovators and their stories. 🚀",
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
            "Debate a topic with friends, trying to see both sides. 🤔",
            "Keep a journal to reflect on your decisions and experiences. 📝",
            "Read non-fiction books about philosophy or history. 📖",
            "Research and analyze a topic you are curious about and share what you learned. 🧐",
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
            "Practice empathy by listening to a friend's problems without judgment. 🤗",
            "Volunteer as a mentor for younger students. 🤝",
            "Read books or watch videos on communication and body language. 🗣️",
            "Write down your feelings and try to understand why you feel that way. 🥰",
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
            "Learn a new software like Photoshop or a video editor. 💻",
            "Create a short film or a podcast with your friends. 🎬",
            "Experiment with digital art, music, or animation. 🎨",
            "Design social media graphics for a school event or club. 📸",
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
            "Do simple science experiments at home. 🧪",
            "Visit a science museum or a planetarium. 🔭",
            "Read articles or books about new scientific discoveries. 🔬",
            "Learn about the stars and planets with an app or a telescope. 🌌",
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
            "Lead a group project at school or in a club. 🤝",
            "Organize a team for a school sport or a community event. 🏆",
            "Read books or articles about famous leaders and their styles. 🗺️",
            "Practice giving constructive feedback to others. 🗣️",
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
            "Try meditation or deep breathing exercises. 🧘",
            "Keep a gratitude journal to focus on positive things. 🙏",
            "Learn about stress management techniques and self-care. 🥰",
            "Practice setting healthy boundaries with your friends and family. ⚖️",
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

    # Calculate the number of questions answered
    answered_count = len([r for r in st.session_state.responses.values() if r is not None])
    total_questions = len(st.session_state.randomized_questions)
    progress_percentage = answered_count / total_questions
    st.progress(progress_percentage)
    st.markdown(f"**Progress:** {answered_count}/{total_questions} questions answered.")

    # Use a unique key for each question based on its content, not its index
    for q_data in st.session_state.randomized_questions:
        question_text = q_data["question"]
        st.session_state.responses[question_text] = st.radio(
            question_text,
            options=["1 - 😞", "2 - 😐", "3 - 👍", "4 - 😄", "5 - 😎"],
            index=None,  # No default selection
            key=question_text,
            horizontal=True # Display radio buttons horizontally for better layout
        )

    st.markdown("---")
    # Only allow submission if all questions have been answered
    if answered_count == total_questions:
        if st.button("Submit Quiz", type="primary"):
            st.session_state.page = "results"
    else:
        st.warning("Please answer all questions before submitting.")


# --- 4. Results page function ---
def show_results():
    """Calculates scores and displays the results page with a radar chart and table."""
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
        response = int(st.session_state.responses[question_text].split(' ')[0])

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
    st.subheader("Top Strengths & Career Paths 🚀")
    top_dims = score_df.head(3)
    st.write("Based on your responses, here are your top three strengths and some ways you can explore them:")

    # Display suggestions for each of the top dimensions
    for _, row in top_dims.iterrows():
        dimension = row['Dimension']
        score = row['Score']
        st.markdown(f"#### **{dimension}** (Score: {score:.2f})")

        # Use an expander to make the content collapsible
        with st.expander("💡 Learning Paths & Activities"):
            st.markdown("Here are some things you can do right now to explore this area:")
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


# --- 5. Page navigation logic ---
if st.session_state.page == "quiz":
    show_quiz()
else:
    show_results()
