def route_request(user_request: str) -> str:
    """
    Route the user's request locally.

    The router is intentionally lightweight.
    It does not use an LLM.
    """

    text = user_request.lower().strip()

    # --------------------------------------------------------
    # Interview preparation
    # --------------------------------------------------------

    interview_keywords = [
        "interview",
        "interview questions",
        "mock interview",
        "prepare me for interview",
        "prepare me for an interview",
        "technical questions",
        "technical interview",
        "hr questions",
        "behavioral questions",
        "interview preparation",
    ]

    # --------------------------------------------------------
    # Resume improvement
    # --------------------------------------------------------

    resume_keywords = [
        "improve my resume",
        "improve resume",
        "rewrite my resume",
        "resume improvement",
        "make my resume better",
        "resume better",
        "resume format",
        "resume bullet",
        "improve my cv",
        "improve cv",
        "rewrite my cv",
        "cv improvement",
    ]

    # --------------------------------------------------------
    # Skill-gap analysis
    # --------------------------------------------------------

    skill_gap_keywords = [
        "skill gap",
        "skill gaps",
        "missing skills",
        "skills am i missing",
        "what skills am i missing",
        "what skills are missing",
        "what skills am i missing for this job",
        "what skills are missing from my resume",
        "what skills do i need",
        "what skills should i learn",
        "what should i learn",
        "what do i lack",
        "what am i missing",
        "missing experience",
        "skills required",
        "skills needed",
        "skills i need",
    ]

    # --------------------------------------------------------
    # Job matching
    # --------------------------------------------------------

    job_match_keywords = [
        "job match",
        "resume match",
        "match my resume",
        "match my resume with",
        "how well does my resume",
        "how well do i match",
        "am i a match",
        "fit this job",
        "fit for this job",
        "suitable for this job",
        "am i suitable",
        "compare my resume",
        "compare resume",
        "job fit",
    ]

    # --------------------------------------------------------
    # Priority order
    # --------------------------------------------------------

    for keyword in interview_keywords:
        if keyword in text:
            return "INTERVIEW_PREP"

    for keyword in resume_keywords:
        if keyword in text:
            return "RESUME_IMPROVEMENT"

    for keyword in skill_gap_keywords:
        if keyword in text:
            return "SKILL_GAP"

    for keyword in job_match_keywords:
        if keyword in text:
            return "JOB_MATCH"

    return "CAREER_GUIDANCE"