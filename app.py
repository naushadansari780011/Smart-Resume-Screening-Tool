from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

required_skills = [
    "python",
    "java",
    "html",
    "css",
    "javascript",
    "sql",
    "machine learning",
    "flask"
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return "No file selected"

    file = request.files["resume"]

    job_description = request.form.get("job_description", "").lower()

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    resume_text = ""

    if file.filename.lower().endswith(".pdf"):

        reader = PdfReader(filepath)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text.lower()

    else:

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            resume_text = f.read().lower()

    matched_skills = []

    for skill in required_skills:
        if skill in resume_text:
            matched_skills.append(skill)

    score = int((len(matched_skills) / len(required_skills)) * 100)

    if job_description:

        jd_skills = []

        for skill in required_skills:
            if skill in job_description:
                jd_skills.append(skill)

        if len(jd_skills) > 0:
            score = int((len(matched_skills) / len(jd_skills)) * 100)

            if score > 100:
                score = 100

    return render_template(
        "result.html",
        filename=file.filename,
        score=score,
        matched_skills=matched_skills
    )


if __name__ == "__main__":
    app.run(debug=True)