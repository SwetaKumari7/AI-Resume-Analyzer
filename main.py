import streamlit as st

from agents.career_agent import run_career_agent
from services.resume_parser import (
    extract_text_from_file,
    clean_resume_text,
    extract_resume_profile,
)


st.set_page_config(
    page_title="AI Resume & Job Assistant",
    page_icon="R",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("AI Resume & Job Assistant")

st.write(
    "Understand how your resume relates to a target job "
    "and get personalized career guidance."
)

st.caption(
    "Supports technical and non-technical jobs."
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        """
This application helps you understand how your resume
relates to a target job.

You can use it for:

- Job matching
- Skill gap analysis
- Interview preparation
- Resume improvement
- Career guidance
        """
    )

    st.divider()

    st.subheader("How it works")

    st.write(
        """
1. Upload your resume
2. Enter the target job
3. Add the job description if available
4. Ask your career question
5. Get personalized analysis
        """
    )


# ---------------------------------------------------------
# STEP 1 - TARGET JOB
# ---------------------------------------------------------

st.header("1. Target Job")

job_role = st.text_input(
    "What job are you applying for?",
    placeholder=(
        "Example: Python Developer, Data Analyst, "
        "Car Washer, Receptionist, Driver"
    ),
)

job_description = st.text_area(
    "Job Description (Optional)",
    placeholder=(
        "Paste the job description here if you have one."
    ),
    height=200,
)


# ---------------------------------------------------------
# STEP 2 - RESUME
# ---------------------------------------------------------

st.header("2. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "txt"],
    help="Supported formats: PDF and TXT",
)


# ---------------------------------------------------------
# STEP 3 - QUESTION
# ---------------------------------------------------------

st.header("3. What do you want to know?")

user_request = st.text_area(
    "Ask your career question",
    placeholder=(
        "Examples:\n"
        "- How well does my resume match this job?\n"
        "- What skills am I missing for this job?\n"
        "- Prepare interview questions for me.\n"
        "- How should I improve my resume for this job?\n"
        "- Give me a learning roadmap for this role."
    ),
    height=140,
)


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

analyze_button = st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

if analyze_button:

    # Validate input

    if not job_role.strip():
        st.error("Please enter the job you are applying for.")
        st.stop()

    if not uploaded_file:
        st.error("Please upload your resume.")
        st.stop()

    if not user_request.strip():
        st.error("Please enter what you want to know.")
        st.stop()

    # Read resume

    with st.spinner("Reading your resume..."):

        try:

            resume_text = extract_text_from_file(
                uploaded_file
            )

            resume_text = clean_resume_text(
                resume_text
            )

        except Exception as error:

            st.error(
                f"Could not read the resume: {error}"
            )

            st.stop()

    if not resume_text:

        st.error(
            "No readable text was found in the resume."
        )

        st.stop()

    # Extract resume profile

    resume_profile = extract_resume_profile(
        resume_text
    )

    # Run career agent

    with st.spinner(
        "Analyzing your resume and the target job..."
    ):

        try:

            result = run_career_agent(
                task=user_request,
                resume_text=resume_text,
                job_role=job_role,
                job_description=job_description,
            )

        except Exception as error:

            st.error(
                f"AI analysis failed: {error}"
            )

            st.stop()

    # -------------------------------------------------
    # JOB UNDERSTANDING
    # -------------------------------------------------

    st.header("Job Understanding")

    if job_description.strip():

        st.caption(
            "The provided job description is the primary "
            "source for understanding the job requirements."
        )

    else:

        st.caption(
            "No job description was provided. "
            "Relevant career knowledge was used."
        )

    requirements = result.get(
        "requirements",
        [],
    )

    st.subheader("Requirements Detected")

    if requirements:

        st.write(
            ", ".join(requirements)
        )

    else:

        st.write(
            "No specific requirements detected."
        )

    # -------------------------------------------------
    # AI ANALYSIS
    # -------------------------------------------------

    st.header("AI Career Analysis")

    st.markdown(
        result.get(
            "answer",
            "No analysis was generated.",
        )
    )

    # -------------------------------------------------
    # EVIDENCE SUMMARY
    # -------------------------------------------------

    found = result.get(
        "evidence_found",
        [],
    )

    gaps = result.get(
        "evidence_gaps",
        [],
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Resume Evidence")

        if found:

            for item in found:

                st.markdown(
                    f"- {item}"
                )

        else:

            st.write(
                "No matching evidence was identified."
            )

    with col2:

        st.subheader("Evidence Gaps")

        if gaps:

            for item in gaps:

                st.markdown(
                    f"- {item}"
                )

        else:

            st.write(
                "No specific evidence gaps were identified."
            )

    # -------------------------------------------------
    # ADDITIONAL DETAILS
    # -------------------------------------------------

    with st.expander("View analysis details"):

        route = result.get(
            "route",
            "UNKNOWN",
        )

        st.write(
            f"Analysis type: {route}"
        )

        st.caption(
            "The request is classified locally before "
            "the AI response is generated."
        )

    with st.expander("View detected resume skills"):

        resume_skills = resume_profile.get(
            "skills",
            [],
        )

        if resume_skills:

            st.write(
                ", ".join(resume_skills)
            )

        else:

            st.write(
                "No known skills were detected automatically."
            )

    sources = result.get(
        "sources",
        [],
    )

    if sources:

        with st.expander(
            "View career knowledge sources"
        ):

            for source in sources:

                st.write(
                    f"- {source}"
                )

    with st.expander(
        "View extracted resume text"
    ):

        st.text(
            resume_text
        )