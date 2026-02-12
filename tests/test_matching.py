from matcher import match_caregivers


def test_matching_ranks_best_candidate_first():
    results = match_caregivers(
        required_specialties=["Tracheostomy", "Seizure Disorders"],
        required_certifications=["RN", "PALS"],
        preferred_language="Spanish",
        acuity_level=5,
        needs_night_shift=True,
    )

    assert results[0]["caregiver"].name in {"Alicia M.", "Nia T."}
    assert results[0]["score"] >= results[-1]["score"]


def test_matching_handles_empty_inputs():
    results = match_caregivers(
        required_specialties=[],
        required_certifications=[],
        preferred_language="",
        acuity_level=3,
        needs_night_shift=False,
    )

    assert len(results) == 4
    assert all("score" in r for r in results)
