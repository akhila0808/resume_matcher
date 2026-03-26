import pdfplumber
import docx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# Extract text from files
# -------------------------------
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            return " ".join([page.extract_text() or "" for page in pdf.pages])

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])

    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()


# -------------------------------
# Skill analysis
# -------------------------------
def analyze_skills(job_skills, resume_skills):
    job_set = set(job_skills)
    resume_set = set(resume_skills)

    matched = list(job_set & resume_set)
    missing = list(job_set - resume_set)
    extra = list(resume_set - job_set)

    return matched, missing, extra


# -------------------------------
# Main processing
# -------------------------------
def process_resumes(job_desc, file_paths):
    results = []

    job_skills = job_desc.lower().split()

    for file_path in file_paths:
        resume_text = extract_text(file_path)
        resume_skills = resume_text.lower().split()

        # Similarity score
        vectorizer = CountVectorizer().fit_transform([job_desc, resume_text])
        score = cosine_similarity(vectorizer)[0][1] * 100

        # Skill comparison
        matched, missing, extra = analyze_skills(job_skills, resume_skills)

        results.append({
            "name": file_path.split("\\")[-1],
            "score": round(score, 2),
            "matched_skills": matched,
            "missing_skills": missing,
            "extra_skills": extra
        })

    return results