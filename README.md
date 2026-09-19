# AI Resume & Job Assistant

An AI-powered career assistant that helps users understand how their resume relates to a target job.

The application combines:

- Resume parsing
- Job requirement extraction
- Evidence-based resume matching
- Skill-gap analysis
- Interview preparation
- Resume improvement guidance
- Career guidance
- RAG-based career knowledge retrieval
- Local LLM-powered responses

The system supports both technical and non-technical occupations.

---

## Project Overview

The goal of this project is to help job seekers answer practical questions such as:

- How well does my resume match this job?
- What skills am I missing?
- What should I learn for this role?
- How should I improve my resume?
- What interview questions should I prepare?
- What does this job require?

Instead of relying entirely on an LLM to make decisions, the application first performs deterministic analysis of the resume and job description.

The LLM is then used to explain the results and provide personalized guidance.

---

# Key Features

### 1. Resume Analysis

Upload a resume in:

- PDF
- TXT

The application extracts and cleans the resume text before analysis.

### 2. Job Analysis

Enter any target job.

Examples:

- Python Developer
- Software Engineer
- Data Analyst
- Machine Learning Engineer
- Receptionist
- Driver
- Car Washer
- Housekeeper

A job description can optionally be provided.

### 3. Job Matching

The application compares detected job requirements with evidence found in the resume.

It identifies:

- Resume evidence
- Evidence gaps
- Relevant requirements

### 4. Skill Gap Analysis

The application identifies requirements from the target job that are not clearly supported by the resume.

It does not automatically assume that a user has a skill that is not present in the resume.

### 5. Interview Preparation

The application can generate interview preparation guidance based on:

- Target job
- Job requirements
- Resume evidence
- Identified gaps
- Career knowledge

### 6. Resume Improvement

The application provides suggestions for improving the resume according to the target job.

### 7. Career Guidance

Users can ask broader questions such as:

```text
Give me a learning roadmap for becoming a stronger Python Developer.