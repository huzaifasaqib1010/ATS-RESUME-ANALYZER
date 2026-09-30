"""
Centralized AI prompts for ATS Resume Analyzer.

Keep prompts separate from app.py so they can be improved without changing
the Streamlit application logic.
"""

import json


OUTPUT_SCHEMA = {
    "overall_score": 0,
    "status": "",
    "summary": "",
    "category_scores": {
        "ats_formatting": 0,
        "keyword_match": 0,
        "professional_summary": 0,
        "work_experience": 0,
        "skills": 0,
        "education_certifications": 0,
        "projects_achievements": 0,
        "content_quality": 0,
    },
    "strengths": [],
    "weaknesses": [],
    "matched_keywords": [],
    "missing_keywords": [],
    "unverified_keywords": [],
    "technical_skills_found": [],
    "technical_skills_missing": [],
    "soft_skills_found": [],
    "soft_skills_missing": [],
    "formatting_issues": [],
    "summary_feedback": "",
    "improved_summary": "",
    "experience_feedback": [],
    "project_feedback": [],
    "education_feedback": [],
    "achievement_feedback": [],
    "grammar_feedback": [],
    "bullet_improvements": [],
    "recommendations": [],
    "final_checklist": [],
}


def build_resume_analysis_prompt() -> str:
    schema = json.dumps(OUTPUT_SCHEMA, indent=2)

    return f"""
You are an expert ATS resume analyst and professional resume reviewer.

Analyze the supplied resume against the supplied target job description.

PRIMARY GOAL:
Determine how well the resume's actual content aligns with the target role
and common ATS-friendly resume practices.

IMPORTANT EVIDENCE RULES:
1. Never invent a skill, certification, employer, education, technology,
   responsibility, achievement, date, or metric.
2. If information is not present in the resume, mark it as missing or
   unverified. Do not assume the candidate lacks it.
3. A missing keyword should only be recommended for addition if the candidate
   genuinely has that skill or experience.
4. Never recommend keyword stuffing or false claims.
5. Do not convert a missing keyword into a claim that the candidate possesses it.
6. Do not predict hiring, interview, salary, or employment outcomes.
7. The score is an estimated resume-to-job compatibility score.
8. Formatting analysis based on extracted text has limitations. Do not claim
   visual formatting problems that cannot reasonably be inferred.
9. Distinguish "not found" from "unverified".
10. Use concise, actionable feedback.

SCORING MODEL:
- ATS Formatting: 0-15
- Keyword Match: 0-25
- Professional Summary: 0-10
- Work Experience: 0-20
- Skills: 0-10
- Education & Certifications: 0-5
- Projects & Achievements: 0-10
- Content Quality: 0-5

The category scores must add up to the overall score.

STATUS:
85-100 = Excellent ATS Compatibility
70-84 = Good
55-69 = Needs Improvement
0-54 = Poor ATS Compatibility

ATS FORMATTING:
Look for evidence of standard headings, readable structure, conventional
section naming, and extraction problems. Do not pretend to see exact visual
layout when only extracted text is available.

KEYWORD ANALYSIS:
Compare the job description with the resume and classify relevant terms as:
- matched
- missing
- unverified

Analyze:
- technical skills
- tools
- certifications
- domain terminology
- soft skills
- relevant responsibilities

WORK EXPERIENCE:
Evaluate:
- relevance
- action verbs
- clarity
- responsibilities
- achievements
- measurable outcomes
- technologies used

When bullets are weak, suggest a stronger version without inventing facts.
If a metric would improve a bullet but none exists, tell the user where a real
metric could be added.

PROFESSIONAL SUMMARY:
Evaluate relevance, specificity, clarity, target-role alignment, and length.
If useful, provide an improved summary based ONLY on facts in the resume.

CONTENT QUALITY:
Check grammar, spelling, repetition, vague language, unnecessary wording,
and professional clarity.

OUTPUT:
Return ONLY valid JSON matching this exact structure:
{schema}

Do not return Markdown.
Do not wrap JSON in ```json fences.
Do not add commentary before or after the JSON.
""".strip()
