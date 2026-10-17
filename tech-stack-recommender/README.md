# Tech Stack Recommender

A beginner-friendly, content-based recommendation web application for DecodeLabs AI Internship Project 3. It compares a user's technical skills with skills listed for technology job roles and returns the top three positive-similarity matches.

## Features
- Responsive web interface with selectable skill chips and custom skill entry
- CSV dataset with 18 technology roles
- Skill normalization, duplicate removal, and unknown-skill reporting
- TF-IDF feature extraction and cosine similarity scoring
- Ranked results with similarity percentages, matched skills, and skills to learn
- Flask JSON API and automated unit tests

## Technologies
Python, Flask, Pandas, scikit-learn, HTML, CSS, JavaScript, CSV.

## How recommendations work
1. **Ingestion:** the user selects at least three skills. The backend normalizes them and removes duplicates.
2. **Feature extraction:** `TfidfVectorizer` creates TF-IDF vectors from the role skill lists. Multiword skills are kept as single features.
3. **Scoring:** cosine similarity compares the user's vector with every job-role vector.
4. **Sorting and filtering:** results are sorted by descending similarity (ties are ordered by role name), zero-score roles are removed, and up to three results are returned.
5. **Skill comparison:** normalized skill sets identify matched skills and skills not currently in the user's profile.

**TF-IDF** gives features more weight when they are informative within the dataset. **Cosine similarity** measures how closely two feature vectors align. This is content-based filtering: it uses the job descriptions and skills rather than past user ratings, so it can make recommendations for a new user who provides an initial skill profile. Scores describe textual alignment only; they are not job-placement probabilities.

## Dataset
`raw_skills.csv` includes `job_role`, `required_skills`, `description`, and `category` columns. The app loads this file with Pandas at startup. Edit or extend the CSV to add roles; keep skill names comma-separated in `required_skills`.

## Project structure
```text
tech-stack-recommender/
├── app.py
├── recommender.py
├── requirements.txt
├── README.md
├── raw_skills.csv
├── templates/index.html
├── static/css/style.css
├── static/js/script.js
└── tests/test_recommender.py
```

## Installation (Windows / VS Code)
Open a terminal in this folder and run:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open the local URL printed by Flask (normally `http://127.0.0.1:5000`). Keep the terminal open while using the app.

## Run tests
With the virtual environment activated:

```bat
python -m unittest discover -s tests -v
```

## API endpoints
- `GET /` — home page
- `GET /api/skills` — supported skill list
- `POST /api/recommend` — recommendations; JSON body example:

```json
{"skills": ["Python", "SQL", "Machine Learning"]}
```

- `GET /api/health` — application/dataset health

## Example
Input: `Python`, `SQL`, `Machine Learning`, `Pandas`. The app calculates actual cosine similarity values and returns up to three positive matches, ranked by score. Exact scores depend on the dataset and are calculated at runtime.

## Troubleshooting
- **Missing package:** activate `venv`, then run `pip install -r requirements.txt`.
- **Dataset error:** make sure `raw_skills.csv` is in the same folder as `app.py` and includes all four required columns.
- **Port already in use:** stop the other Flask process, or change the port in the `app.run(...)` line.
- **No matches:** choose at least three supported skills. Unknown skills are reported and not used for matching.

## Limitations
- The recommendations depend on the coverage and quality of the sample CSV dataset.
- Similarity is based on skill text, not labor-market demand, experience, qualifications, or personal preferences.
- This is not a trained predictive model and does not use deep learning or external AI services.

## Future enhancements
- Add more roles and reviewed skill taxonomies
- Allow users to filter by work area or experience level
- Add downloadable recommendation reports and user feedback
