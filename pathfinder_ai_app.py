import streamlit as st
import pandas as pd
import openai
import datetime

st.set_page_config(page_title="Pathfinder.AI", layout="wide")
st.title("🚀 Pathfinder.AI — Your AI Career Advisor")

# Load API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.markdown("---")

# --- USER INPUT FORM ---
with st.form("career_form", clear_on_submit=False):
    name = st.text_input("👤 Your Full Name")

    experience_years = st.slider("🧠 Years of Experience", 0, 30, 0)
    if experience_years <= 1:
        level = "Fresh Graduate"
    elif experience_years <= 5:
        level = "Early Career"
    elif experience_years <= 10:
        level = "Mid Career"
    else:
        level = "Senior Level"

    degree_count = st.selectbox("🎓 How many degrees do you have?", [1, 2, 3])
    degrees = []
    for i in range(degree_count):
        col1, col2, col3 = st.columns(3)
        with col1:
            deg_type = st.selectbox(f"Degree {i+1} Type", ["Diploma", "Bachelor's", "Master's", "PhD"], key=f"deg_type_{i}")
        with col2:
            major = st.text_input(f"Major {i+1}", key=f"major_{i}")
        with col3:
            university = st.text_input(f"University {i+1}", key=f"uni_{i}")
        degrees.append(f"{deg_type} in {major} from {university}")

    skills = st.multiselect("💡 Your Skills", ["Python", "SQL", "Machine Learning", "Data Analysis", "Cybersecurity", "Cloud Computing", "Project Management", "UX/UI"], key="skills")
    other_skill = st.text_input("Other Skill (if any)")
    if other_skill:
        skills.append(other_skill)

    cert_files = st.file_uploader("📎 Upload any certifications (optional)", type=["pdf", "jpg", "png"], accept_multiple_files=True)

    employment_status = st.text_area("💼 What's your current employment situation and what do you aspire to work in?")
    career_shift = st.text_area("🔁 Are you switching careers? If so, from what to what?")

    submitted = st.form_submit_button("🔍 Generate Career Roadmap")

# --- RESPONSE GENERATION ---
if submitted:
    with st.spinner("Thinking..."):
        # Save to CSV
        user_data = {
            "Name": name,
            "Experience": experience_years,
            "Level": level,
            "Degrees": " | ".join(degrees),
            "Skills": ", ".join(skills),
            "EmploymentStatus": employment_status,
            "CareerShift": career_shift,
            "Timestamp": datetime.datetime.now()
        }
        df = pd.DataFrame([user_data])
        try:
            existing = pd.read_csv("submissions.csv")
            updated = pd.concat([existing, df], ignore_index=True)
        except:
            updated = df
        updated.to_csv("submissions.csv", index=False)

        # Prompt AI
        prompt = f"""
        I am an AI career assistant. Based on the following info, give me a tailored roadmap.

        Name: {name}
        Experience Level: {level}
        Years of Experience: {experience_years}
        Degrees: {', '.join(degrees)}
        Skills: {', '.join(skills)}
        Employment Situation: {employment_status}
        Career Shift: {career_shift}

        I want a realistic and accurate output. Do not recommend advanced certifications like PMP to fresh graduates. Recommend suitable certifications, programs, and job platforms for this person. Also suggest a 3-6 month learning path.
        """

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.subheader("🎯 Personalized AI Career Roadmap")
        st.write(response.choices[0].message.content)

# --- Footer ---
st.markdown("---")
st.caption("By using this website, you agree that your data may be stored to improve the tool and notify you of future opportunities.")
