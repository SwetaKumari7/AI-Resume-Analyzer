import re
from typing import Dict, List


# Common skills and practical job-related terms.
SKILL_KEYWORDS = [
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "html",
    "css",
    "react",
    "django",
    "flask",
    "fastapi",
    "git",
    "github",
    "docker",
    "aws",
    "excel",
    "microsoft excel",
    "communication",
    "customer service",
    "sales",
    "cash handling",
    "cleaning",
    "housekeeping",
    "laundry",
    "driving",
    "vehicle cleaning",
    "car washing",
    "car washer",
    "washing",
    "vacuuming",
    "vehicle care",
    "equipment handling",
    "maintenance",
    "inventory",
    "data entry",
    "typing",
    "accounting",
    "bookkeeping",
    "teaching",
    "childcare",
    "cooking",
    "security",
    "machine operation",
    "welding",
    "plumbing",
    "electrical work",
    "attention to detail",
    "time management",
    "teamwork",
    "problem solving",
    "punctuality",
    "reliability",
    "responsibility",
]


def _contains_term(
    text: str,
    term: str,
) -> bool:
    """
    Check whether a term appears as a complete word/phrase.

    This prevents false matches such as:

    C -> car
    C -> cleaning
    SQL -> SQL-based
    """

    pattern = (
        r"(?<![A-Za-z0-9+#])"
        + re.escape(term)
        + r"(?![A-Za-z0-9+#])"
    )

    return re.search(
        pattern,
        text,
        re.IGNORECASE,
    ) is not None


def _extract_skills(
    text: str,
) -> List[str]:
    """
    Detect relevant skills from the job title
    and job description.
    """

    found = []

    for skill in SKILL_KEYWORDS:

        if _contains_term(
            text,
            skill,
        ):

            found.append(skill)

    # Handle C separately.
    # Only match standalone programming language C.
    if re.search(
        r"(?<![A-Za-z])C(?![A-Za-z])",
        text,
    ):

        found.append("C")

    return found


def _extract_bullets(
    text: str,
) -> List[str]:
    """
    Extract responsibilities written as bullets.
    """

    lines = text.splitlines()

    bullets = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith(
            ("-", "*", "•")
        ):

            cleaned = line.lstrip(
                "-*• "
            ).strip()

            if cleaned:
                bullets.append(
                    cleaned
                )

    return bullets


def _extract_responsibilities(
    text: str,
) -> List[str]:
    """
    Extract responsibilities from bullet-style
    and paragraph-style job descriptions.
    """

    bullets = _extract_bullets(
        text
    )

    if bullets:

        return bullets[:8]

    responsibility_patterns = [
        r"responsibilities include\s+(.+?)(?:\.|$)",
        r"duties include\s+(.+?)(?:\.|$)",
        r"responsible for\s+(.+?)(?:\.|$)",
        r"role includes\s+(.+?)(?:\.|$)",
    ]

    results = []

    for pattern in responsibility_patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:

            # Split common list separators.
            parts = re.split(
                r",|\band\b",
                match,
                flags=re.IGNORECASE,
            )

            for part in parts:

                cleaned = part.strip()

                if len(cleaned) <= 3:
                    continue

                # Remove common leading words.
                cleaned = re.sub(
                    r"^(including|such as)\s+",
                    "",
                    cleaned,
                    flags=re.IGNORECASE,
                )

                # Remove unnecessary leading "and".
                cleaned = re.sub(
                    r"^and\s+",
                    "",
                    cleaned,
                    flags=re.IGNORECASE,
                )

                cleaned = cleaned.strip()

                if not cleaned:
                    continue

                # Capitalize only the first character.
                cleaned = (
                    cleaned[0].upper()
                    + cleaned[1:]
                )

                if cleaned not in results:
                    results.append(
                        cleaned
                    )

    return results[:8]


def _extract_experience(
    text: str,
) -> str:
    """
    Extract simple experience requirements.
    """

    pattern = (
        r"(\d+(?:\.\d+)?)\s*"
        r"(?:\+)?\s*years?"
        r"(?:\s+of)?\s+experience"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if match:

        return (
            f"{match.group(1)} years "
            "of experience"
        )

    return "Not specified"


def _extract_education(
    text: str,
) -> str:
    """
    Detect common education requirements.
    """

    education_terms = [
        "b.tech",
        "bachelor",
        "degree",
        "diploma",
        "12th",
        "10th",
        "graduate",
        "postgraduate",
        "master",
        "mba",
        "mca",
        "bca",
    ]

    found = []

    for term in education_terms:

        if _contains_term(
            text,
            term,
        ):

            found.append(term)

    if not found:
        return "Not specified"

    return ", ".join(found)


def analyze_job(
    job_title: str,
    job_description: str = "",
) -> Dict[str, object]:
    """
    Analyze any job locally.

    The job description is the primary source
    when it is provided.
    """

    job_title = job_title.strip()
    job_description = job_description.strip()

    if not job_title:

        raise ValueError(
            "Job title cannot be empty."
        )

    combined_text = (
        f"{job_title}\n"
        f"{job_description}"
    )

    skills = _extract_skills(
        combined_text
    )

    responsibilities = (
        _extract_responsibilities(
            job_description
        )
    )

    experience = _extract_experience(
        job_description
    )

    education = _extract_education(
        job_description
    )

    if job_description:

        description_note = (
            "The job description was provided "
            "and is the primary source for this analysis."
        )

    else:

        description_note = (
            "No job description was provided. "
            "The analysis is based mainly on the "
            "job title and general career knowledge."
        )

    return {
        "job_title": job_title,
        "job_description": job_description,
        "skills": skills,
        "responsibilities": responsibilities,
        "experience": experience,
        "education": education,
        "description_note": description_note,
    }