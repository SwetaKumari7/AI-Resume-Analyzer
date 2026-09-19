# AI Resume & Job Assistant

An AI-powered career assistant that helps users understand how their resume matches a target job, identify skill gaps, prepare for interviews, improve their resume, and get career guidance.

The project uses a **local LLM, RAG, resume parsing, job analysis, and lightweight request routing** to provide personalized career assistance.

---

## Features

### Resume Analysis
- Upload PDF or TXT resumes
- Extract resume text
- Detect common resume sections
- Identify known skills

### Job Analysis
- Enter a target job
- Add a job description
- Extract required skills
- Identify responsibilities
- Detect experience and education requirements

### Job Matching
Compare the requirements of a job with evidence found in the resume.

Example:

```text
Job requires:
Python, Django, MySQL, Git

Resume contains:
Python, Django, MySQL, Git

Result:
Matching evidence found