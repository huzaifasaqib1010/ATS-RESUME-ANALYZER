# ATS Resume Analyzer AI — Streamlit Workflow

## 1. Project Architecture

```text
ats-resume-analyzer/
│
├── app.py
├── prompts.py
├── workflow.md
├── requirements.txt
└── .gitignore
```

### File responsibilities

| File | Responsibility |
|---|---|
| `app.py` | Main Streamlit application, file extraction, Groq integration, scoring validation, UI and reports |
| `prompts.py` | Central AI system prompt and expected JSON structure |
| `workflow.md` | Development, testing and deployment documentation |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Keeps secrets/cache files out of GitHub |

---

# 2. End-to-End Workflow

```text
User
  │
  ▼
Streamlit UI
  │
  ├── Upload Resume
  │       │
  │       ▼
  │   PDF/DOCX/TXT extraction
  │       │
  │       ▼
  │   Clean Resume Text
  │
  ├── Paste/Upload Job Description
  │
  ├── Target Job Title
  │
  └── Years of Experience
          │
          ▼
       app.py
          │
          ▼
      prompts.py
          │
          ▼
       Groq API
          │
          ▼
    Structured JSON
          │
          ▼
  Validate + Normalize Scores
          │
          ▼
      Streamlit Results
          │
          ├── ATS Score
          ├── Category Scores
          ├── Keywords
          ├── Skills
          ├── Experience
          ├── Formatting
          ├── Recommendations
          └── Download Report
```

---

# 3. ATS Scoring

The application uses a transparent 100-point framework:

```text
ATS Formatting          15
Keyword Match           25
Professional Summary    10
Work Experience         20
Skills                   10
Education & Certifications 5
Projects & Achievements 10
Content Quality          5
                         ---
                         100
```

The score is an estimated resume-to-job compatibility score.

It is NOT:

- a hiring probability
- an interview probability
- a guarantee of ATS selection
- a guarantee of employment

---

# 4. User Workflow

## Step 1 — Upload Resume

Supported:

- PDF
- DOCX
- TXT

The application extracts the text.

If the PDF is image-only/scanned, normal text extraction may return nothing. OCR can be added later.

---

## Step 2 — Add Job Description

The user can:

- paste the job description, or
- upload a PDF/DOCX/TXT job description.

Providing a job description enables job-specific keyword analysis.

Without a job description, the app can still analyze resume quality, but keyword matching is less specific.

---

## Step 3 — Add Target Job

Example:

```text
Python Developer
```

Optional:

```text
2 years
```

---

## Step 4 — Analyze

The application sends:

```text
Resume Text
+
Job Description
+
Target Job
+
Experience
```

to Groq.

The system prompt in `prompts.py` instructs the AI to return structured JSON.

---

# 5. AI Response

The AI returns:

```text
Overall score
Status
Summary
Category scores
Strengths
Weaknesses
Matched keywords
Missing keywords
Unverified keywords
Technical skills
Soft skills
Formatting issues
Summary feedback
Improved summary
Experience feedback
Project feedback
Education feedback
Achievement feedback
Grammar feedback
Bullet improvements
Recommendations
Final checklist
```

`app.py` validates the response before displaying it.

---

# 6. Why Prompts Are Separate

Do not put the large AI prompt directly inside the Streamlit UI.

Instead:

```python
from prompts import build_resume_analysis_prompt
```

This makes prompt engineering easier.

You can later create:

```text
prompts.py
```

with multiple prompts:

```text
resume_analysis_prompt
summary_rewrite_prompt
bullet_rewrite_prompt
cover_letter_prompt
```

without making `app.py` unnecessarily large.

---

# 7. Streamlit Secrets

Never commit your API key to GitHub.

For Streamlit deployment, open the application's Secrets configuration and add:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
GROQ_MODEL = "YOUR_CURRENT_GROQ_MODEL"
```

The model must be one that is currently available to your Groq account.

The app also supports environment variables:

```text
GROQ_API_KEY
GROQ_MODEL
```

---

# 8. Local/Colab Testing

Install:

```bash
pip install -r requirements.txt
```

Set credentials:

```python
import os

os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"
os.environ["GROQ_MODEL"] = "YOUR_AVAILABLE_MODEL"
```

Run:

```bash
streamlit run app.py
```

---

# 9. GitHub Deployment

Create a GitHub repository:

```text
ats-resume-analyzer
```

Upload:

```text
app.py
prompts.py
requirements.txt
workflow.md
.gitignore
```

Do NOT upload:

```text
.env
```

or any file containing an API key.

---

# 10. Streamlit Deployment

On Streamlit hosting:

1. Connect your GitHub repository.
2. Select `app.py` as the main application file.
3. Deploy.
4. Add `GROQ_API_KEY` to Streamlit Secrets.
5. Add `GROQ_MODEL` to Streamlit Secrets.
6. Restart/redeploy the application.

The runtime reads the secrets automatically.

---

# 11. Recommended `.gitignore`

Create a `.gitignore` containing:

```text
.env
__pycache__/
*.pyc
.streamlit/secrets.toml
.DS_Store
```

---

# 12. Testing Checklist

Before deployment test:

### File extraction

- [ ] PDF works
- [ ] DOCX works
- [ ] TXT works
- [ ] Empty/scanned PDF gives a clear message
- [ ] Unsupported files are rejected

### AI

- [ ] API key is detected
- [ ] Model is configurable
- [ ] Valid JSON is returned
- [ ] Invalid JSON is handled
- [ ] API errors are displayed clearly

### Scoring

- [ ] Score is 0–100
- [ ] Category scores respect their maximums
- [ ] Category total equals overall score
- [ ] Status matches the score

### UI

- [ ] Resume upload works
- [ ] Job description works
- [ ] Analyze button works
- [ ] Results display correctly
- [ ] Tabs work
- [ ] Reports download correctly

### Deployment

- [ ] No API key is committed
- [ ] `requirements.txt` installs
- [ ] Streamlit starts with `app.py`
- [ ] Streamlit Secrets are configured

---

# 13. Future Versions

After the MVP works, possible additions include:

```text
V2
├── Resume rewriting
├── Bullet point rewriting
├── Cover letter generator
├── Job description keyword extractor
├── Resume section completeness score
└── PDF report

V3
├── Multiple resume versions
├── Resume history
├── User accounts
├── Saved job descriptions
├── Resume comparison
└── Dashboard

V4
├── Subscription system
├── Usage limits
├── Payment integration
├── Admin dashboard
└── Analytics
```

Build the MVP first. Do not add these features until the basic upload → extraction → AI → score → report workflow is stable.
