from typing import Dict, List, Tuple
import re

from agents.router_agent import route_request
from rag.retriever import retrieve_documents
from services.llm_service import generate_response


TECHNICAL_SOURCE_MAP = {
    "python developer": "python_developer.txt",
    "python development": "python_developer.txt",
    "software engineer": "software_engineer.txt",
    "software developer": "software_engineer.txt",
    "machine learning engineer": "machine_learning_engineer.txt",
    "ml engineer": "machine_learning_engineer.txt",
    "data scientist": "data_scientist.txt",
}


REQUIREMENT_ALIASES = {
    "python": ["python"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "rest APIs": ["rest api", "rest apis", "restful api", "restful apis"],
    "mysql": ["mysql"],
    "sql": ["sql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb"],
    "git": ["git", "github"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "javascript": ["javascript"],
    "typescript": ["typescript"],
    "react": ["react"],
    "data structures": ["data structures"],
    "algorithms": ["algorithms"],
    "machine learning": ["machine learning"],
    "deep learning": ["deep learning"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "opencv": ["opencv"],
    "attention to detail": ["attention to detail"],
    "reliability": ["reliability", "reliable"],
    "punctuality": ["punctuality", "punctual"],
    "responsibility": ["responsibility", "responsible"],
    "teamwork": ["teamwork", "team work", "team player"],
    "problem solving": ["problem solving", "problem-solving"],
    "communication": ["communication", "communication skills"],
    "customer service": ["customer service"],
    "sales": ["sales"],
    "cash handling": ["cash handling"],
    "cleaning": ["cleaning"],
    "vehicle cleaning": ["vehicle cleaning", "cleaning vehicles", "vehicle cleaner"],
    "vacuuming": ["vacuuming", "vacuum", "vacuuming vehicles"],
    "cleaning equipment": ["cleaning equipment", "cleaning tools"],
    "driving": ["driving", "driver"],
    "inventory": ["inventory", "stock management"],
    "data entry": ["data entry"],
    "typing": ["typing"],
    "accounting": ["accounting"],
    "bookkeeping": ["bookkeeping"],
    "teaching": ["teaching"],
    "childcare": ["childcare", "child care"],
    "cooking": ["cooking"],
    "security": ["security"],
    "machine operation": ["machine operation", "machine operator"],
    "welding": ["welding"],
    "plumbing": ["plumbing"],
    "electrical work": ["electrical work"],
    "clean and maintainable code": [
        "clean and maintainable code",
        "clean, maintainable code",
        "maintainable code",
        "clean code",
    ],
}

SOFT_SKILLS = {
    "reliability",
    "punctuality",
    "responsibility",
    "teamwork",
    "communication",
    "attention to detail",
}

TECHNICAL_CONTEXT_WORDS = {
    "authentication", "system", "software", "model", "verification",
    "algorithm", "code", "project", "application", "security",
    "network", "api", "service", "performance", "testing",
    "development", "database", "implementation", "workflow",
}


def _normalize_text(text: str) -> str:
    text = text or ""
    text = text.replace("\u00ad", "")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def _term_in_text(text: str, term: str) -> bool:
    text = _normalize_text(text)
    term = _normalize_text(term)
    if not term:
        return False
    pattern = r"(?<![a-z0-9+#])" + re.escape(term) + r"(?![a-z0-9+#])"
    return re.search(pattern, text, re.IGNORECASE) is not None


def _soft_skill_evidence(text: str, skill: str) -> bool:
    """Count soft-skill evidence only when it is not technical-context wording."""
    normalized = _normalize_text(text)

    for alias in REQUIREMENT_ALIASES.get(skill, [skill]):
        pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
        for match in re.finditer(pattern, normalized, re.IGNORECASE):
            start = max(0, match.start() - 130)
            end = min(len(normalized), match.end() + 130)
            context = normalized[start:end]

            if any(word in context for word in TECHNICAL_CONTEXT_WORDS):
                continue

            return True

    return False


def _find_resume_evidence(resume_text: str, requirement: str) -> bool:
    if requirement in SOFT_SKILLS:
        return _soft_skill_evidence(resume_text, requirement)

    aliases = REQUIREMENT_ALIASES.get(requirement, [requirement])
    return any(_term_in_text(resume_text, alias) for alias in aliases)


def _get_technical_source(job_role: str) -> str | None:
    role = _normalize_text(job_role)
    for title, source in TECHNICAL_SOURCE_MAP.items():
        if title in role:
            return source
    return None


def _extract_jd_requirements(job_role: str, job_description: str) -> List[str]:
    """Extract explicit requirements from the supplied job description only."""
    text = _normalize_text(job_description)
    requirements: List[str] = []

    for canonical, aliases in REQUIREMENT_ALIASES.items():
        if any(_term_in_text(text, alias) for alias in aliases):
            requirements.append(canonical)

    role = _normalize_text(job_role)

    # Generic "cleaning" or the job title itself is not a useful Car Washer skill.
    if "car washer" in role or "vehicle cleaner" in role:
        requirements = [
            item for item in requirements
            if item not in {"cleaning", "car washer", "washing"}
        ]

        if any(
            phrase in text
            for phrase in (
                "vehicle cleaning",
                "cleaning vehicles",
                "cleaning cars",
                "cleaning car",
                "washing vehicles",
                "washing cars",
            )
        ) and "vehicle cleaning" not in requirements:
            requirements.append("vehicle cleaning")

        if "vacuum" in text and "vacuuming" not in requirements:
            requirements.append("vacuuming")

        if (
            "cleaning equipment" in text or "cleaning tools" in text
        ) and "cleaning equipment" not in requirements:
            requirements.append("cleaning equipment")

    title_requirements = {
        "car washer",
        "vehicle cleaner",
        "python developer",
        "software engineer",
        "software developer",
        "data scientist",
        "machine learning engineer",
        "ml engineer",
    }
    requirements = [
        item for item in requirements
        if item not in title_requirements
    ]

    return requirements


def _extract_knowledge_requirements(content: str) -> List[str]:
    """Extract canonical requirements from a relevant career-guide section."""
    requirements: List[str] = []
    lines = content.splitlines()
    collecting = False

    headings = {
        "CORE SKILLS:",
        "IMPORTANT SUPPORTING SKILLS:",
        "IMPORTANT SKILLS:",
        "COMMON QUALITIES:",
        "ENGINEERING SKILLS:",
        "AI SKILLS:",
        "PROGRAMMING:",
    }

    stop_headings = {
        "WEB DEVELOPMENT:",
        "DATABASES:",
        "IMPORTANT INTERVIEW TOPICS:",
        "COMMON INTERVIEW TOPICS:",
        "TYPICAL SKILL GAPS:",
        "PROJECTS:",
        "USEFUL PROJECTS:",
        "PROJECT EXPECTATIONS:",
        "POSSIBLE SKILL GAPS:",
        "TRANSFERABLE SKILLS:",
        "RESUME PRINCIPLE:",
        "AI SKILLS:",
    }

    for line in lines:
        stripped = line.strip()
        upper = stripped.upper()

        if upper in headings:
            collecting = True
            continue

        if upper in stop_headings:
            collecting = False

        if not collecting:
            continue

        for piece in re.split(r",|;|•", stripped):
            piece = piece.strip(" .:-")
            if not piece:
                continue

            for canonical, aliases in REQUIREMENT_ALIASES.items():
                if any(_term_in_text(piece, alias) for alias in aliases):
                    if canonical not in requirements:
                        requirements.append(canonical)
                    break

    return requirements


def _get_requirements(job_role: str, job_description: str) -> Tuple[List[str], List[str]]:
    """Return authoritative requirements and the knowledge sources used."""
    if job_description.strip():
        # With a JD, the JD is authoritative. Do not add generic RAG requirements.
        return _extract_jd_requirements(job_role, job_description), []

    source = _get_technical_source(job_role) or "general_jobs.txt"
    results = retrieve_documents(query=job_role, top_k=3)

    selected = next(
        (result for result in results if result["source"] == source),
        None,
    )

    if selected is None and results:
        selected = results[0]

    if selected is None:
        return [], []

    return (
        _extract_knowledge_requirements(selected["content"]),
        [selected["source"]],
    )


def _format_items(items: List[str]) -> str:
    if not items:
        return "- None explicitly identified."
    return "\n".join(f"- {item}" for item in items)


def _understanding(task: str, job_role: str) -> str:
    route = route_request(task)
    messages = {
        "SKILL_GAP": (
            f"You asked which requirements you are missing for the "
            f"{job_role} role based on the supplied job description and resume."
        ),
        "JOB_MATCH": (
            f"You asked how your resume compares with the requirements "
            f"for the {job_role} role."
        ),
        "INTERVIEW_PREP": (
            f"You asked for interview preparation for the {job_role} role."
        ),
        "RESUME_IMPROVEMENT": (
            f"You asked how to improve your resume for the {job_role} role."
        ),
        "CAREER_GUIDANCE": (
            f"You asked for career guidance related to the {job_role} role."
        ),
    }
    return messages.get(route, messages["CAREER_GUIDANCE"])


def _next_steps(task: str, job_role: str, gaps: List[str]) -> str:
    if not gaps:
        return (
            "No skill gaps were identified from the supplied job requirements "
            "and resume evidence. You can focus on practicing and demonstrating "
            "the requirements that were already found."
        )

    gap_text = "\n".join(f"- {gap}" for gap in gaps)
    prompt = f"""
You are helping a candidate with a job application.

Job: {job_role}
User request: {task}

The deterministic system found these exact resume evidence gaps:
{gap_text}

Give short practical advice about ONLY these gaps.
Do not add any other missing skills.
Do not mention generic career-guide gaps.
Do not use a heading.
Keep the answer under 150 words.
""".strip()

    try:
        return generate_response(
            prompt=prompt,
            system_instruction=(
                "The evidence gaps are fixed facts. Never invent additional gaps."
            ),
        ).strip()
    except Exception:
        return (
            "Focus on developing and demonstrating these requirements: "
            + ", ".join(gaps)
            + "."
        )


def run_career_agent(
    task: str,
    resume_text: str,
    job_role: str,
    job_description: str = "",
) -> Dict[str, object]:
    route = route_request(task)
    requirements, sources = _get_requirements(job_role, job_description)

    evidence_found = [
        requirement
        for requirement in requirements
        if _find_resume_evidence(resume_text, requirement)
    ]
    evidence_gaps = [
        requirement
        for requirement in requirements
        if requirement not in evidence_found
    ]

    if route == "SKILL_GAP":
        answer = (
            "## Understanding\n\n"
            f"{_understanding(task, job_role)}\n\n"
            "## What The Evidence Shows\n\n"
            f"{_format_items(evidence_found)}\n\n"
            "## Evidence-Based Skill Gaps\n\n"
            f"{_format_items(evidence_gaps)}\n\n"
            "## What To Learn Next\n\n"
            f"{_next_steps(task, job_role, evidence_gaps)}"
        )
    else:
        facts = (
            f"Job: {job_role}\n"
            f"Request type: {route}\n"
            f"Requirements: {', '.join(requirements) or 'None detected'}\n"
            f"Evidence found: {', '.join(evidence_found) or 'None'}\n"
            f"Evidence gaps: {', '.join(evidence_gaps) or 'None'}"
        )
        prompt = f"""
Provide concise guidance for this career request.

{facts}

User request:
{task}

The requirements, evidence found, and evidence gaps are deterministic facts.
Do not add, remove, or reinterpret them.
If discussing missing skills, discuss only the listed evidence gaps.
""".strip()

        try:
            guidance = generate_response(
                prompt=prompt,
                system_instruction=(
                    "Use deterministic evidence as facts. Never invent resume evidence "
                    "or missing requirements."
                ),
            ).strip()
        except Exception:
            guidance = "Review the deterministic evidence and identified gaps above."

        answer = (
            "## Understanding\n\n"
            f"{_understanding(task, job_role)}\n\n"
            "## What The Evidence Shows\n\n"
            f"{_format_items(evidence_found)}\n\n"
            "## Evidence-Based Skill Gaps\n\n"
            f"{_format_items(evidence_gaps)}\n\n"
            "## AI Guidance\n\n"
            f"{guidance}"
        )

    return {
        "answer": answer,
        "route": route,
        "requirements": requirements,
        "evidence_found": evidence_found,
        "evidence_gaps": evidence_gaps,
        "sources": sources,
    }
