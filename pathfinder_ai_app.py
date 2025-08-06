import streamlit as st
import pandas as pd
import openai
import datetime

# Language setup
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

def toggle_lang():
    st.session_state.lang = "ع" if st.session_state.lang == "EN" else "EN"

st.set_page_config(page_title="Pathfinder.AI", layout="wide")

# Language switch button top-right
col_lang1, col_lang2 = st.columns([9, 1])
with col_lang2:
    st.button(st.session_state.lang, on_click=toggle_lang)

# Text content dictionary for EN and AR (simplified example)
texts = {
    "EN": {
        "title": "🚀 Pathfinder.AI — Your AI Career Advisor",
        "name": "👤 Your Full Name",
        "experience": "🧠 Years of Experience",
        "degree_count": "🎓 How many degrees do you have?",
        "degree_type": "Degree {i} Type",
        "major": "Major {i}",
        "university": "University {i}",
        "skills": "💡 Your Skills",
        "other_skill": "Other Skill (if any)",
        "languages": "🗣️ Languages You Speak",
        "brief": "📝 Brief About Yourself (Optional)",
        "upload_cert": "📎 Upload any certifications (optional)",
        "employment_status": "💼 What's your current employment situation and what do you aspire to work in?",
        "career_shift": "🔁 Are you switching careers? If so, from what to what?",
        "submit": "🔍 Generate Career Roadmap",
        "personalized": "🎯 Personalized AI Career Roadmap",
        "footer": "By using this website, you agree that your data may be stored to improve the tool and notify you of future opportunities.",
        "made_by": "Made by Saudi hands 🇸🇦"
    },
    "ع": {
        "title": "🚀 باثفايندر.ايه آي — مستشارك المهني بالذكاء الاصطناعي",
        "name": "👤 الاسم الكامل",
        "experience": "🧠 سنوات الخبرة",
        "degree_count": "🎓 كم عدد شهاداتك؟",
        "degree_type": "نوع الشهادة {i}",
        "major": "التخصص {i}",
        "university": "الجامعة {i}",
        "skills": "💡 مهاراتك",
        "other_skill": "مهارة أخرى (إن وجدت)",
        "languages": "🗣️ اللغات التي تتحدثها",
        "brief": "📝 نبذة عن نفسك (اختياري)",
        "upload_cert": "📎 ارفع أي شهادات (اختياري)",
        "employment_status": "💼 وضعك الوظيفي الحالي وما تطمح للعمل به؟",
        "career_shift": "🔁 هل تغير مسارك المهني؟ إذا نعم، من ماذا إلى ماذا؟",
        "submit": "🔍 انشئ خطة مهنية",
        "personalized": "🎯 خطة مهنية شخصية بالذكاء الاصطناعي",
        "footer": "باستخدام هذا الموقع، أنت توافق على تخزين بياناتك لتحسين الأداة وإعلامك بالفرص المستقبلية.",
        "made_by": "صنع بأيدي سعودية 🇸🇦"
    }
}

t = texts[st.session_state.lang]

st.title(t["title"])

st.markdown("---")

# --- USER INPUT FORM ---
with st.form("career_form", clear_on_submit=False):
    name = st.text_input(t["name"])

    experience_years = st.slider(t["experience"], 0, 30, 0)
    if experience_years <= 1:
        level = "Fresh Graduate" if st.session_state.lang == "EN" else "خريج جديد"
    elif experience_years <= 5:
        level = "Early Career" if st.session_state.lang == "EN" else "بداية المسار المهني"
    elif experience_years <= 10:
        level = "Mid Career" if st.session_state.lang == "EN" else "متوسط المسار المهني"
    else:
        level = "Senior Level" if st.session_state.lang == "EN" else "مستوى متقدم"

    degree_count = st.selectbox(t["degree_count"], [1, 2, 3, 4, 5])
    degrees = []
    for i in range(degree_count):
        col1, col2, col3 = st.columns(3)
        with col1:
            deg_type = st.selectbox(
                t["degree_type"].format(i=i+1),
                ["Highschool or below", "Diploma", "Bachelor's", "Master's", "PhD"],
                key=f"deg_type_{i}"
            )
        with col2:
            major = st.text_input(t["major"].format(i=i+1), key=f"major_{i}")
        with col3:
            university = st.text_input(t["university"].format(i=i+1), key=f"uni_{i}")
        degrees.append(f"{deg_type} in {major} from {university}")

    # New skills list with non-tech options + autocomplete
    skill_options = [
        "Python", "SQL", "Machine Learning", "Data Analysis", "Cybersecurity",
        "Cloud Computing", "Project Management", "UX/UI",
        "Marketing", "Sales", "Finance", "Human Resources", "Graphic Design",
        "Writing", "Public Speaking", "Languages", "Leadership", "Customer Service"
    ]
    skills = st.multiselect(t["skills"], skill_options, key="skills")

    other_skill = st.text_input(t["other_skill"])
    if other_skill and other_skill not in skills:
        skills.append(other_skill)

    # Languages spoken multi-select (example list)
    language_options = ["Arabic", "English", "French", "Spanish", "Chinese", "Hindi", "Other"]
    languages = st.multiselect(t["languages"], language_options, key="languages")

    brief = st.text_area(t["brief"], max_chars=300)

    cert_files = st.file_uploader(t["upload_cert"], type=["pdf", "jpg", "png"], accept_multiple_files=True)

    employment_status = st.text_area(t["employment_status"])
    career_shift = st.text_area(t["career_shift"])

    submitted = st.form_submit_button(t["submit"])

# --- RESPONSE GENERATION ---
if submitted:
    with st.spinner("Thinking..."):
        user_data = {
            "Name": name,
            "Experience": experience_years,
            "Level": level,
            "Degrees": " | ".join(degrees),
            "Skills": ", ".join(skills),
            "Languages": ", ".join(languages),
            "Brief": brief,
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

        prompt = f"""
        I am an AI career assistant. Based on the following info, give me a tailored roadmap.

        Name: {name}
        Experience Level: {level}
        Years of Experience: {experience_years}
        Degrees: {', '.join(degrees)}
        Skills: {', '.join(skills)}
        Languages: {', '.join(languages)}
        Brief: {brief}
        Employment Situation: {employment_status}
        Career Shift: {career_shift}

        I want a realistic and accurate output. Do not recommend advanced certifications like PMP to fresh graduates. Recommend suitable certifications, programs, and job platforms for this person. Also suggest a 3-6 month learning path.
        """

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.subheader(t["personalized"])
        st.write(response.choices[0].message.content)

# --- Footer ---
st.markdown("---")
st.markdown(
    f'<p style="font-size:10px; color:gray; opacity:0.6;">{t["footer"]}</p>',
    unsafe_allow_html=True
)
st.markdown(
    f'<p style="font-size:9px; color:gray; opacity:0.4; text-align:center;">{t["made_by"]}</p>',
    unsafe_allow_html=True
)
