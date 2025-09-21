# ResuMatch – Automated Resume Relevance Checker

ResuMatch is a web-based application that evaluates resumes against job descriptions to generate a **Relevance Score**, highlight **missing skills**, and provide a **suitability verdict**. This helps placement teams shortlist candidates quickly and gives students personalized feedback to improve their resumes.

---

## 🚀 Features

- **Upload Resumes & Job Descriptions** – Supports PDF, DOCX, and TXT formats.
- **Hard Match Analysis** – Keyword & skill matching (AWS, Python, Machine Learning, etc.).
- **Semantic Match Analysis** – AI-powered embeddings to check contextual fit between resumes and job descriptions.
- **Relevance Score** – Weighted score combining hard and soft matches (0–100).
- **Verdict** – High / Medium / Low suitability.
- **Missing Skills** – Highlights skills or keywords not present in the resume.
- **Results Dashboard** – View all analyzed resumes filtered by Job ID.
- **Professional UI** – Clean, modern, and responsive design using Streamlit.

---

## 🧰 Tech Stack

**Backend:**

- Python 3.10+
- FastAPI – API backend
- Pinecone – Vector database for semantic embeddings
- SentenceTransformers – Generating embeddings for resumes and JDs
- PyPDF2 / python-docx – Extract text from resumes
- FuzzyWuzzy – Hard keyword matching

**Frontend:**

- Streamlit – Interactive dashboard for uploading and viewing results
- Pandas – Display results in tabular format

**Database:**

- SQLite – Stores analyzed resume results (can be replaced with PostgreSQL for production)

---

## 📂 Folder Structure

ResuMatch/
├── backend/
│ ├── main.py # FastAPI backend
│ ├── relevance.py # Core relevance scoring logic
│ ├── resume_parser.py # Resume text extraction
│ ├── jd_parser.py # JD text extraction
│ └── database.py # Database functions
├── frontend/
│ └── app.py # Streamlit frontend
├── data/ # Sample resumes & job descriptions
├── .gitignore
├── .env.example
└── README.md

---

## ⚡ Getting Started
1. Clone the repository

git clone https://github.com/codermisba/resumatch.git
cd ResuMatch

2. Create a virtual environment & install dependencies

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt

3. Set up environment variables
Create a .env file based on .env.example:
PINECONE_API_KEY=your_pinecone_api_key_here

4. Run the backend
cd backend
uvicorn main:app --reload

5. Run the frontend
cd frontend
streamlit run app.py
Open http://localhost:8501 in your browser.

📝 Usage
Enter Candidate Name and Job ID.

Upload Resume and Job Description (or paste JD text).

Click Analyze Resume to see the relevance score, missing skills, and verdict.

Use the Results Dashboard to fetch all analyzed resumes for a Job ID.

🌟 Future Improvements
Add user authentication for placement teams.

Integrate email notifications for students with feedback.

Use PostgreSQL for large-scale deployment.

Deploy on Heroku / Streamlit Cloud / AWS for production.

📄 License
This project is licensed under the MIT License. See LICENSE file for details.
