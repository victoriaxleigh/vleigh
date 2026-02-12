from flask import Flask, render_template, request

from matcher import match_caregivers, tokenize_csv

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    matches = None

    if request.method == "POST":
        required_specialties = tokenize_csv(request.form.get("specialties", ""))
        required_certifications = tokenize_csv(request.form.get("certifications", ""))
        preferred_language = request.form.get("language", "").strip()
        acuity_level = int(request.form.get("acuity_level", 3))
        needs_night_shift = bool(request.form.get("night_shift"))

        matches = match_caregivers(
            required_specialties=required_specialties,
            required_certifications=required_certifications,
            preferred_language=preferred_language,
            acuity_level=acuity_level,
            needs_night_shift=needs_night_shift,
        )

    return render_template("index.html", matches=matches)


if __name__ == "__main__":
    app.run(debug=True)
