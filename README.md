# Pediatric Complex Caregiver Matching App

A lightweight AI-style matching web app that helps families and care coordinators find caregivers for pediatric patients with highly complex needs.

## Features

- Intake form for high-acuity pediatric requirements.
- Explainable matching score (0-100) based on:
  - specialty overlap,
  - certification overlap,
  - acuity alignment,
  - years of experience,
  - language preference,
  - overnight availability.
- Ranked caregiver results with transparent "why this match" explanations.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Open `http://127.0.0.1:5000`.


## Instant preview (no dependencies)

If you want a quick visual preview without installing Flask dependencies:

```bash
python -m http.server 8000
```

Then open:
- `http://127.0.0.1:8000/preview.html` (static demo preview)
- `http://127.0.0.1:8000/templates/index.html` (raw template only)

## Tests

```bash
pytest
```
