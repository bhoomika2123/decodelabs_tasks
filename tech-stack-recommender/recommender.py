"""Content-based career recommendations using TF-IDF and cosine similarity."""
from pathlib import Path
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATASET_PATH = Path(__file__).resolve().parent / "raw_skills.csv"
ALIASES = {
    "ml": "machine learning", "ai": "artificial intelligence", "js": "javascript",
    "postgres": "postgresql", "scikit learn": "scikit-learn", "powerbi": "power bi",
    "rest api": "rest apis", "api": "apis", "html5": "html", "css3": "css",
    "amazon web services": "aws", "cloud": "cloud computing", "data viz": "data visualization",
    "ux": "ux research", "ui": "ui design", "ci cd": "ci/cd",
}

def normalize_skill(value: str) -> str:
    """Normalize whitespace/case and common aliases while preserving unknown input."""
    text = re.sub(r"\s+", " ", str(value or "").strip().lower())
    return ALIASES.get(text, text)

def split_skills(value) -> list[str]:
    if pd.isna(value) or not str(value).strip():
        return []
    return list(dict.fromkeys(normalize_skill(s) for s in str(value).split(",") if normalize_skill(s)))

class RecommendationEngine:
    def __init__(self, dataset_path=DATASET_PATH):
        self.dataset_path = Path(dataset_path)
        self.df = None
        self.vectorizer = None
        self.role_matrix = None
        self.supported_skills = set()
        self.load_dataset()

    def load_dataset(self):
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
        df = pd.read_csv(self.dataset_path).fillna("")
        required = {"job_role", "required_skills", "description", "category"}
        if not required.issubset(df.columns) or df.empty:
            raise ValueError("Dataset must contain job_role, required_skills, description, and category columns with at least one row.")
        df = df[df["job_role"].astype(str).str.strip().ne("")].copy()
        if df.empty:
            raise ValueError("Dataset contains no valid job roles.")
        df["_skills"] = df["required_skills"].apply(split_skills)
        self.df = df.reset_index(drop=True)
        self.supported_skills = {skill for skills in self.df["_skills"] for skill in skills}
        # The pipe separator preserves multiword skills as single features.
        documents = [" | ".join(skills) for skills in self.df["_skills"]]
        self.vectorizer = TfidfVectorizer(tokenizer=lambda text: text.split(" | "), token_pattern=None, lowercase=False)
        self.role_matrix = self.vectorizer.fit_transform(documents)

    def get_supported_skills(self):
        return sorted(self.supported_skills)

    def recommend(self, skills, top_n=3):
        if not isinstance(skills, list):
            raise ValueError("Skills must be provided as a list.")
        cleaned = list(dict.fromkeys(normalize_skill(s) for s in skills if str(s or "").strip()))
        if len(cleaned) < 3:
            raise ValueError("Please enter at least three skills.")
        recognized = [s for s in cleaned if s in self.supported_skills]
        unknown = [s for s in cleaned if s not in self.supported_skills]
        if len(recognized) < 3:
            raise ValueError("Please provide at least three supported skills. Check the unrecognized skills list and try supported names.")
        user_vector = self.vectorizer.transform([" | ".join(recognized)])
        scores = cosine_similarity(user_vector, self.role_matrix).flatten()
        ranked = sorted(enumerate(scores), key=lambda pair: (-pair[1], str(self.df.iloc[pair[0]]["job_role"]).lower()))
        results = []
        for index, score in ranked:
            if score <= 0:
                continue
            row = self.df.iloc[index]
            role_skills = row["_skills"]
            matched = [s for s in role_skills if s in recognized]
            missing = [s for s in role_skills if s not in recognized]
            results.append({"job_role": str(row["job_role"]), "similarity": round(float(score), 4),
                "similarity_percent": round(float(score) * 100, 1), "category": str(row["category"]),
                "description": str(row["description"]), "required_skills": role_skills,
                "matched_skills": matched, "missing_skills": missing})
            if len(results) >= max(1, int(top_n)):
                break
        message = "Recommendations are based on textual skill alignment, not job-placement probability or a guarantee of career success."
        if not results:
            message = "No relevant job-role matches were found. Try adding more supported skills."
        elif len(results) < min(3, top_n):
            message = f"Only {len(results)} relevant match(es) were found. " + message
        return {"success": True, "selected_skills": cleaned, "recognized_skills": recognized,
                "unrecognized_skills": unknown, "recommendations": results, "message": message}
