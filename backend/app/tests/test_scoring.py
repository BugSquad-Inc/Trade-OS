import pytest
from app.services.scoring_service import score_match, grade_from_score

class DummyCompany:
    canonical_name = "Picard GmbH"
    segment = "Leather goods"

class DummyExporter:
    company_name = "Butler's Leather"
    eudr_readiness_score = 68

def test_grade_boundaries():
    assert grade_from_score(90.0) == "A"
    assert grade_from_score(85.0) == "A"
    assert grade_from_score(84.9) == "B"
    assert grade_from_score(70.0) == "B"
    assert grade_from_score(55.0) == "C"
    assert grade_from_score(50.0) == "D"

def test_score_match_structure():
    score = score_match(DummyCompany(), DummyExporter(), rank=1)
    assert score.total_score == 92.0
    assert score.grade == "A"
    assert score.score_version == "v2.0-product-matrix"
    assert len(score.drivers) == 5
    assert score.product_fit_score == 23.5
    assert score.compliance_score == 23.5
    assert score.lane_economics_score == 18.0
    assert score.intent_signals_score == 13.5
    assert score.accessibility_score == 13.5
    assert len(score.counter_factuals) > 0
    assert len(score.key_gaps) > 0
    assert score.next_best_action is not None
