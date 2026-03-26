from flask import Flask, render_template, request
import os
import sys

# ✅ Add project root to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# ✅ Absolute import (this will work now)
from utils.process import process_resumes

app = Flask(__name__)

UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        job_desc = request.form.get("job_description")
        files = request.files.getlist("resumes")

        file_paths = []

        for file in files:
            if file.filename != "":
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                file_paths.append(file_path)

        if job_desc and file_paths:
            results = process_resumes(job_desc, file_paths)

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
