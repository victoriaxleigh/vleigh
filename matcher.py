from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Caregiver:
    name: str
    certifications: List[str]
    specialties: List[str]
    years_experience: int
    acuity_level: int  # 1-5
    languages: List[str]
    telehealth: bool
    night_shift: bool
    location: str


CAREGIVERS: list[Caregiver] = [
    Caregiver(
        name="Alicia M.",
        certifications=["RN", "PALS", "Ventilator Care"],
        specialties=["Tracheostomy", "Seizure Disorders", "G-Tube"],
        years_experience=11,
        acuity_level=5,
        languages=["English", "Spanish"],
        telehealth=True,
        night_shift=True,
        location="Chicago, IL",
    ),
    Caregiver(
        name="Priya K.",
        certifications=["RN", "CPR", "Pediatric Oncology"],
        specialties=["Immunocompromised Care", "Central Line", "Pain Management"],
        years_experience=8,
        acuity_level=4,
        languages=["English", "Hindi"],
        telehealth=False,
        night_shift=True,
        location="Naperville, IL",
    ),
    Caregiver(
        name="Daniel R.",
        certifications=["LPN", "CPR", "Home Vent Support"],
        specialties=["Respiratory Support", "G-Tube", "Mobility Support"],
        years_experience=6,
        acuity_level=4,
        languages=["English"],
        telehealth=True,
        night_shift=False,
        location="Evanston, IL",
    ),
    Caregiver(
        name="Nia T.",
        certifications=["RN", "PALS", "Pediatric Neuro Care"],
        specialties=["Seizure Disorders", "Medication Complexity", "Tracheostomy"],
        years_experience=14,
        acuity_level=5,
        languages=["English", "French"],
        telehealth=True,
        night_shift=True,
        location="Oak Park, IL",
    ),
]


WEIGHTS = {
    "specialty": 35,
    "certification": 20,
    "acuity": 20,
    "experience": 10,
    "language": 10,
    "schedule": 5,
}


def tokenize_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def match_caregivers(
    required_specialties: list[str],
    required_certifications: list[str],
    preferred_language: str,
    acuity_level: int,
    needs_night_shift: bool,
) -> list[dict]:
    required_specialties_set = {s.lower() for s in required_specialties}
    required_certifications_set = {c.lower() for c in required_certifications}

    matches = []
    for caregiver in CAREGIVERS:
        score = 0
        reasons: list[str] = []

        specialty_overlap = len(
            required_specialties_set.intersection({s.lower() for s in caregiver.specialties})
        )
        if required_specialties_set:
            specialty_ratio = specialty_overlap / len(required_specialties_set)
            score += specialty_ratio * WEIGHTS["specialty"]
        if specialty_overlap > 0:
            reasons.append(f"{specialty_overlap} specialty match(es)")

        cert_overlap = len(
            required_certifications_set.intersection(
                {c.lower() for c in caregiver.certifications}
            )
        )
        if required_certifications_set:
            cert_ratio = cert_overlap / len(required_certifications_set)
            score += cert_ratio * WEIGHTS["certification"]
        if cert_overlap > 0:
            reasons.append(f"{cert_overlap} certification match(es)")

        acuity_distance = abs(caregiver.acuity_level - acuity_level)
        acuity_score = max(0, WEIGHTS["acuity"] - (acuity_distance * 5))
        score += acuity_score
        reasons.append(f"acuity support level {caregiver.acuity_level}/5")

        exp_score = min(WEIGHTS["experience"], caregiver.years_experience)
        score += exp_score

        if preferred_language and preferred_language.lower() in {
            l.lower() for l in caregiver.languages
        }:
            score += WEIGHTS["language"]
            reasons.append(f"speaks {preferred_language}")

        if needs_night_shift and caregiver.night_shift:
            score += WEIGHTS["schedule"]
            reasons.append("night-shift availability")
        elif not needs_night_shift:
            score += WEIGHTS["schedule"]

        match_percentage = min(100, round(score, 1))
        matches.append(
            {
                "caregiver": caregiver,
                "score": match_percentage,
                "reasons": reasons,
            }
        )

    matches.sort(key=lambda m: m["score"], reverse=True)
    return matches
