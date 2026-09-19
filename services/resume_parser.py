import io
import re
from typing import Dict, List

import PyPDF2


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF resume.
    """

    pdf_bytes = uploaded_file.read()

    reader = PyPDF2.PdfReader(
        io.BytesIO(pdf_bytes)
    )

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages).strip()


def extract_text_from_file(uploaded_file) -> str:
    """
    Extract text from PDF or TXT files.
    """

    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)

    return uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    ).strip()


def clean_resume_text(text: str) -> str:
    """
    Clean unnecessary whitespace from extracted resume text.
    """

    text = re.sub(
        r"\r\n?",
        "\n",
        text
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def extract_resume_profile(
    text: str,
) -> Dict[str, List[str]]:
    """
    Extract a basic structured profile from the resume.

    This is intentionally lightweight.
    The LLM will perform deeper analysis later.
    """

    text_lower = text.lower()

    known_skills = [
        "python",
        "java",
        "c",
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
        "next.js",
        "django",
        "flask",
        "fastapi",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "keras",
        "opencv",
        "nlp",
        "rag",
        "llm",
        "generative ai",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "pandas",
        "numpy",
        "scikit-learn",
    ]

    found_skills = []

    for skill in known_skills:
        if skill in text_lower:
            found_skills.append(skill)

    sections = {}

    section_names = [
        "education",
        "skills",
        "projects",
        "experience",
        "internship",
        "certifications",
        "achievements",
    ]

    lines = text.splitlines()

    current_section = "general"

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        matched_section = None

        for section in section_names:

            if (
                section in lower_line
                and len(clean_line) < 50
            ):
                matched_section = section
                break

        if matched_section:

            current_section = matched_section

            sections.setdefault(
                current_section,
                []
            )

        else:

            sections.setdefault(
                current_section,
                []
            ).append(clean_line)

    return {
        "skills": found_skills,
        "sections": sections,
    }