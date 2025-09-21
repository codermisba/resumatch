from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from fuzzywuzzy import fuzz
from sentence_transformers.util import cos_sim
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

# ---------------------------
# 1. Initialize Pinecone
# ---------------------------
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "jd-embeddings"

pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(INDEX_NAME)

# ---------------------------
# 2. Load embedding model
# ---------------------------
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ---------------------------
# 3. Hard Match Scoring with fuzzy matching
# ---------------------------
def hard_match_score(resume_text: str, keywords: list, threshold=70) -> float:
    scores = []
    for kw in keywords:
        best_ratio = 0
        for line in resume_text.splitlines():
            ratio = fuzz.partial_ratio(kw.lower(), line.lower())
            best_ratio = max(best_ratio, ratio)
        scores.append(1 if best_ratio >= threshold else 0)
    return sum(scores) / len(keywords) if keywords else 0

# ---------------------------
# 4. Semantic Match
# ---------------------------
def semantic_match_score(resume_text: str, jd_text: str, job_id: str) -> float:
    # Encode resume
    resume_emb = embed_model.encode(resume_text, normalize_embeddings=True)

    # Fetch JD embedding safely
    fetch_result = index.fetch(ids=[job_id]).vectors
    if job_id not in fetch_result:
        # Upsert JD embedding if missing
        jd_emb = embed_model.encode(jd_text, normalize_embeddings=True)
        index.upsert([{
            "id": job_id,
            "values": jd_emb.tolist(),
            "metadata": {"text": jd_text}
        }])
        jd_vector = jd_emb
    else:
        jd_vector = fetch_result[job_id].values

    # Cosine similarity
    score = cos_sim(resume_emb, jd_vector).item()
    return score

# ---------------------------
# 5. Compute Relevance
# ---------------------------
def compute_relevance(resume_text: str, jd_text: str, keywords: list, job_id: str):
    hard = hard_match_score(resume_text, keywords)
    soft = semantic_match_score(resume_text, jd_text, job_id)

    # Weighted final score
    final_score = 0.6 * hard + 0.4 * soft
    final_score_percentage = round(final_score * 100, 2)  # scale 0-100

    # Verdict
    if final_score >= 0.7:
        verdict = "High"
    elif final_score >= 0.4:
        verdict = "Medium"
    else:
        verdict = "Low"

    # Identify missing keywords using fuzzy matching
    missing = []
    for kw in keywords:
        found = any(fuzz.partial_ratio(kw.lower(), line.lower()) >= 70 for line in resume_text.splitlines())
        if not found:
            missing.append(kw)

    # Feedback string
    feedback = f"Missing keywords: {', '.join(missing) if missing else 'None'}. Hard match: {hard:.2f}, Semantic match: {soft:.2f}."

    return final_score_percentage, verdict, missing, feedback
