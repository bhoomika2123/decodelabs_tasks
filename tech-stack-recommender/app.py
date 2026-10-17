from flask import Flask, jsonify, render_template, request
from recommender import RecommendationEngine

app = Flask(__name__)
try:
    engine = RecommendationEngine()
    DATA_ERROR = None
except (FileNotFoundError, ValueError, OSError) as exc:
    engine = None
    DATA_ERROR = str(exc)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok" if engine else "error", "dataset_loaded": engine is not None}), (200 if engine else 503)

@app.get("/api/skills")
def skills():
    if not engine:
        return jsonify({"success": False, "message": "The dataset could not be loaded."}), 503
    return jsonify({"success": True, "skills": engine.get_supported_skills()})

@app.post("/api/recommend")
def recommend():
    if not engine:
        return jsonify({"success": False, "message": "The dataset could not be loaded. Check raw_skills.csv."}), 503
    if not request.is_json:
        return jsonify({"success": False, "message": "Send a JSON request containing a skills list."}), 400
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        return jsonify({"success": False, "message": "The request must contain a skills list."}), 400
    try:
        return jsonify(engine.recommend(data["skills"]))
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except Exception:
        app.logger.exception("Recommendation request failed")
        return jsonify({"success": False, "message": "Something went wrong while generating recommendations."}), 500

if __name__ == "__main__":
    app.run(debug=True)
