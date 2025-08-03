import streamlit as st
import openai
import os

# ---- CONFIGURATION ----
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="PathFinder.AI", layout="centered")
st.title("🎯 PathFinder.AI: Your AI Career Advisor")
st.markdown("_Get personalized career paths, learning roadmaps, and internship suggestions powered by AI._")

# ---- USER INPUT ----
st.subheader("Tell us about yourself")
gpa = st.text_input("GPA", max_chars=4)
skills = st.text_area("List your skills (comma-separated)")
interests = st.text_area("What are your interests?")
career_goal = st.text_input("Career goal (optional)")

# ---- BUILD PROMPT ----
def build_prompt(gpa, skills, interests, goal):
    return f"""
    I’m building a career roadmap for a computer science student. Here are their details:
    - GPA: {gpa}
    - Skills: {skills}
    - Interests: {interests}
    - Career goal: {goal if goal else "Not sure yet"}

    Based on this, suggest:
    1. Top 3 career options
    2. A 6-month personalized learning roadmap with specific courses/resources
    3. Project or internship ideas for each career
    4. Recommended certifications or achievements

    Format your response clearly with bullet points and sections.
    """

# ---- GENERATE OUTPUT ----
if st.button("🧠 Generate My Career Path"):
    if not gpa or not skills or not interests:
        st.warning("Please fill in at least GPA, skills, and interests.")
    else:
        with st.spinner("Thinking... 🧠"):
            try:
                prompt = build_prompt(gpa, skills, interests, career_goal)
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful and professional AI career advisor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                result = response.choices[0].message.content
                st.success("Here’s your personalized career path 👇")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")
