import pytest
from app.services.scoring_service import score_match, ScoreDriver, CounterFactualRecommendation

class DummyCompany:
    canonical_name = "Bader GmbH & Co. KG"
    segment = "Automotive Leather"

class DummyExporter:
    company_name = "Butler's Leather"
    eudr_readiness_score = 95

def test_non_compensatory_compliance_gate_failure():
    # Test 1: Chemical failure with Chromium VI > 3.0 ppm
    failing_score = score_match(
        buyer=DummyCompany(),
        exporter=DummyExporter(),
        rank=1,
        chromium_vi_ppm=4.8, # Exceeds 3.0 ppm limit!
        reach_compliant=True
    )
    assert failing_score.is_compliance_gate_failed is True
    assert failing_score.compliance_score == 0.0
    assert failing_score.total_score <= 38.0
    assert failing_score.grade == "D"
    assert "Hexavalent Chromium" in (failing_score.compliance_gate_reason or "")
    
    # Verify counter-factual provides immediate remedy recommendation
    assert len(failing_score.counter_factuals) > 0
    first_cf = failing_score.counter_factuals[0]
    assert first_cf.dimension == "Compliance"
    assert "Cr VI" in first_cf.action
    assert first_cf.score_impact_pts > 20.0

def test_non_compensatory_reach_failure():
    # Test 2: REACH non-compliant
    reach_failing = score_match(
        buyer=DummyCompany(),
        exporter=DummyExporter(),
        rank=1,
        chromium_vi_ppm=0.0,
        reach_compliant=False
    )
    assert reach_failing.is_compliance_gate_failed is True
    assert reach_failing.compliance_score == 0.0
    assert reach_failing.grade == "D"

def test_counter_factual_generation_and_explainability():
    # Test 3: Normal passed evaluation
    passed_score = score_match(
        buyer=DummyCompany(),
        exporter=DummyExporter(),
        rank=3,
        chromium_vi_ppm=0.0,
        reach_compliant=True
    )
    assert passed_score.is_compliance_gate_failed is False
    assert passed_score.compliance_score > 20.0
    assert passed_score.total_score >= 80.0
    assert passed_score.score_version == "v2.0-product-matrix"

    # Verify explainability drivers have weights summing to 100
    total_weights = sum(d.weight for d in passed_score.drivers)
    assert total_weights == 100

    # Verify counter-factual suggestions have positive impacts
    for cf in passed_score.counter_factuals:
        assert cf.score_impact_pts > 0
        assert cf.projected_total_score > passed_score.total_score
        assert len(cf.implementation_tip) > 10
