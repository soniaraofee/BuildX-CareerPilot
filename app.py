import streamlit as st

from jobs import load_jobs, filter_jobs_by_role
from career_agent import (
    analyze_jobs,
    generate_application,
    refine_recommendations,
    improve_resume,
)
from auth import (
    init_db,
    register_user,
    login_user,
    get_user_id,
    get_profile,
    save_profile,
)


st.set_page_config(
    page_title="CareerPilot",
    page_icon="🎯",
    layout="centered",
)
init_db()

# -------------------------
# Session State
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None
if "profile" not in st.session_state:
    st.session_state.profile = None

if "result" not in st.session_state:
    st.session_state.result = None

if "jobs" not in st.session_state:
    st.session_state.jobs = None

if "application" not in st.session_state:
    st.session_state.application = None
if "resume_improvement" not in st.session_state:
    st.session_state.resume_improvement = None
# -------------------------
# Authentication
# -------------------------

if not st.session_state.logged_in:

    st.title("🎯 CareerPilot")

    st.write(
        "AI career companion for finding the right opportunities."
    )

    tab_login, tab_register = st.tabs(
        ["🔐 Login", "📝 Register"]
    )


# -------------------------
# Login
# -------------------------

    with tab_login:

        login_username = st.text_input(
            "Username",
            key="login_username",
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
        ):

            if login_user(
                login_username,
                login_password,
            ):

                st.session_state.logged_in = True
                st.session_state.username = login_username

                st.session_state.user_id = get_user_id(
                    login_username
                )
                st.session_state.profile = get_profile(
                    st.session_state.user_id
                )

                st.success(
                    "Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

# -------------------------
# Register
# -------------------------

    with tab_register:

        register_username = st.text_input(
            "Choose a username",
            key="register_username",
        )

        register_password = st.text_input(
            "Choose a password",
            type="password",
            key="register_password",
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
        ):

            if not register_username or not register_password:

                st.warning(
                    "Please enter a username and password."
                )

            elif register_user(
                register_username,
                register_password,
            ):

                st.success(
                    "Account created successfully! You can now log in."
                )

            else:

                st.error(
                    "This username already exists."
                )


    st.stop()
# -------------------------
# App Header
# -------------------------

st.title("🎯 CareerPilot")
if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_id = None
    st.session_state.profile = None
    st.session_state.result = None
    st.session_state.jobs = None
    st.session_state.application = None
    st.session_state.resume_improvement = None
    st.rerun()

st.write(
    "Your AI career companion for finding the right opportunities."
)

st.divider()


# -------------------------
# Candidate Profile
# -------------------------

st.header("👤 Your Career Profile")

saved_profile = st.session_state.profile or {}
name = st.text_input(
    "Your name",
    value=saved_profile.get("name", ""),
    placeholder="e.g. Sonia",
)

education = st.text_input(
    "Education",
    value=saved_profile.get("education", ""),
    placeholder="e.g. Computer Engineering student",
)

skills = st.text_input(
    "Your skills",
    value=saved_profile.get("skills", ""),
    placeholder="e.g. Python, C++, Git, Linux",
)

experience = st.text_area(
    "Experience / Projects",
    value=saved_profile.get("experience", ""),
    placeholder="Describe your projects or work experience...",
)

resume = st.text_area(
    "📄 Resume",
    value=saved_profile.get("resume", ""),
    placeholder="Paste your resume text here...",
    height=200,
)

role_options = [
    "Backend Development",
    "Frontend Development",
    "Data Analysis",
    "AI / Machine Learning",
    "C++ / Software Development",
]

saved_role = saved_profile.get(
    "target_role",
    role_options[0],
)

target_role = st.selectbox(
    "🎯 Target role",
    role_options,
    index=(
        role_options.index(saved_role)
        if saved_role in role_options
        else 0
    ),
)

work_options = [
    "Remote",
    "On-site",
    "Either",
]

saved_work_type = saved_profile.get(
    "work_type",
    work_options[0],
)

work_type = st.selectbox(
    "💼 Preferred work type",
    work_options,
    index=(
        work_options.index(saved_work_type)
        if saved_work_type in work_options
        else 0
    ),
)


st.divider()


# -------------------------
# Find Opportunities
# -------------------------

if st.button(
    "🚀 Find My Opportunities",
    use_container_width=True,
):

    if not name or not education or not skills:

        st.warning(
            "Please fill in your name, education and skills."
        )

    else:

        profile = {
        "name": name,
        "education": education,
        "skills": skills,
        "experience": experience,
        "resume": resume,
        "target_role": target_role,
        "work_type": work_type,
        }
        save_profile(
            st.session_state.user_id,
            profile,
        )

        with st.spinner(
            "🤖 CareerPilot is analyzing opportunities..."
        ):

            jobs = load_jobs()

            filtered_jobs = filter_jobs_by_role(
                jobs,
                target_role,
            )

            result = analyze_jobs(
                profile,
                filtered_jobs,
            )

        st.session_state.profile = profile
        st.session_state.jobs = jobs
        st.session_state.result = result

        # Reset previous application
        st.session_state.application = None


# -------------------------
# Display Results
# -------------------------

if st.session_state.result is not None:

    result = st.session_state.result
    jobs = st.session_state.jobs
    profile = st.session_state.profile


    st.success(
        "Career analysis completed!"
    )

    st.divider()

    st.header(
        "🎯 CareerPilot's Recommendations"
    )


# -------------------------
# Job Recommendations
# -------------------------

    for job in result.jobs:

        st.subheader(
            f"{job.title} — {job.company}"
        )

        st.metric(
            "Match Score",
            f"{job.match_score}/100"
        )

        st.write(
            job.why
        )

        if job.missing_skills:

            st.write(
                "**Missing skills:**"
            )

            for skill in job.missing_skills:

                st.write(
                    f"- {skill}"
                )

        st.divider()


# -------------------------
# Top Recommendation
# -------------------------

    st.header(
        "🏆 Top Recommendation"
    )

    st.success(
        result.top_recommendation
    )


    # -------------------------
    # Action Tip
    # -------------------------

    st.header(
        "💡 Action Tip"
    )

    st.info(
        result.action_tip
    )

# -------------------------
# User Feedback
# -------------------------

st.divider()

st.header(
    "🔄 Refine Your Recommendations"
)

feedback = st.text_area(
    "What would you like CareerPilot to improve or change?",
    placeholder=(
        "For example: I prefer remote jobs, "
        "and I want to focus more on Python backend roles."
    ),
)

if st.button(
    "🔄 Refine Recommendations",
    use_container_width=True,
):

    if not feedback.strip():

        st.warning(
            "Please enter your feedback first."
        )

    else:

       with st.spinner(
    "CareerPilot is refining your recommendations..."
    ):
        refined_result = refine_recommendations(
            profile,
            st.session_state.jobs,
            st.session_state.result,
            feedback,
        )

    st.session_state.result = refined_result
    st.session_state.application = None
    with st.spinner(
    "CareerPilot is improving your resume..."
    ):
        resume_improvement = improve_resume(
            profile,
            feedback,
        )

    st.session_state.resume_improvement = resume_improvement

    st.success(
        "Recommendations successfully refined based on your feedback!"
    )

    st.rerun()

    resume_improvement = st.session_state.get(
    "resume_improvement"
)

# -------------------------
# Resume Improvement
# -------------------------

resume_improvement = st.session_state.get(
    "resume_improvement"
)

if resume_improvement is not None:

    st.divider()

    st.header("📄 Resume Improvement")

    st.subheader("✨ Improved Summary")
    st.write(
        resume_improvement.improved_summary
    )

    st.subheader("💪 Skills to Highlight")

    for skill in resume_improvement.highlighted_skills:
        st.write(f"- {skill}")

    st.subheader("🛠️ Suggested Changes")

    for change in resume_improvement.suggested_changes:
        st.write(f"- {change}")
    # -------------------------
    # Select an Opportunity
    # -------------------------

    st.divider()

    st.header(
        "🔎 Explore an Opportunity"
    )

    job_options = [
        f"{job.title} — {job.company}"
        for job in result.jobs
    ]

    selected_job = st.selectbox(
        "Choose an opportunity to explore:",
        job_options,
    )

    selected_index = job_options.index(
        selected_job
    )

    selected_job_data = result.jobs[selected_index]


    # Find original job data
    selected_job_full = next(
        job
        for job in jobs
        if (
            job["title"] == selected_job_data.title
            and job["company"] == selected_job_data.company
        )
    )


    st.subheader(
        f"📌 {selected_job_data.title}"
    )

    st.write(
        f"**Company:** {selected_job_data.company}"
    )

    st.write(
        f"**Match Score:** {selected_job_data.match_score}/100"
    )

    st.write(
        "**Why this job matches:**"
    )

    st.write(
        selected_job_data.why
    )


    if selected_job_data.missing_skills:

        st.write(
            "**Skills you should improve:**"
        )

        for skill in selected_job_data.missing_skills:

            st.write(
                f"- {skill}"
            )


# -------------------------
# Application Preparation
# -------------------------

st.divider()

st.header(
    "📝 Prepare My Application"
)

if st.button(
    "🤖 Generate Application Preparation",
    use_container_width=True,
):

    with st.spinner(
        "CareerPilot is preparing your application..."
    ):

        application = generate_application(
            profile,
            selected_job_full,
        )

    st.session_state.application = application


# Display Application
application = st.session_state.get("application")

if application is not None:

    st.success(
        "Application preparation completed!"
    )

    st.subheader(
        "📝 Application Summary"
    )

    st.write(
        application.summary
    )

    st.subheader(
        "💪 Your Strengths"
    )

    for strength in application.strengths:

        st.write(
            f"- {strength}"
        )

    st.subheader(
        "🎯 Focus Areas"
    )

    for area in application.focus_areas:

        st.write(
            f"- {area}"
        )